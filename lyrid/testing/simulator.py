import uuid
from contextlib import suppress
from typing import Any

from lyrid import Ask, BackgroundTaskExited, ChildStopped
from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessStoppedSignal
from .background_task import BackgroundTask
from .captor import Captor
from .error_message import specifying_both_return_value_and_exception_is_not_allowed, \
    either_key_or_address_of_the_child_must_be_specified_and_not_both


class Simulator:
    def __init__(self, actor_address: Address, process: ActorProcess, captor: Captor):
        self._actor_address = actor_address
        self._process = process
        self._captor = captor

    def tell(self, message: Message, by: Address):
        with suppress(ProcessStoppedSignal):
            self._process.receive(by, message)

    def ask(self, message: Message) -> str:
        ref_id = uuid.uuid4().hex
        self._process.receive(Address("$"), Ask(message, ref_id=ref_id))
        return ref_id

    def run_background_task(self, background_task: BackgroundTask, notify_actor: bool = True):
        try:
            return_value = background_task.task(*background_task.args)
            msg = BackgroundTaskExited(background_task.task_id, return_value=return_value)
        except Exception as e:
            msg = BackgroundTaskExited(background_task.task_id, exception=e)

        if notify_actor:
            self._process.receive(self._actor_address, msg)

    def run_all_background_tasks(self, notify_actor: bool = True):
        for background_task in self._captor.get_background_tasks():
            self.run_background_task(background_task, notify_actor=notify_actor)

    def background_task_exit(self, task_id: str, *, return_value: Any = None, exception: Exception = None):
        if return_value is not None and exception is not None:
            raise TypeError(specifying_both_return_value_and_exception_is_not_allowed)

        self._process.receive(self._actor_address, BackgroundTaskExited(
            task_id, return_value=return_value, exception=exception,
        ))

    def child_stop(self, key: str = None, address: Address = None, *, exception: Exception = None):
        if address is None:
            if key is None:
                raise TypeError(either_key_or_address_of_the_child_must_be_specified_and_not_both)
            address = self._actor_address.child(key)
        elif key is not None:
            raise TypeError(either_key_or_address_of_the_child_must_be_specified_and_not_both)
        self._process.receive(self._actor_address, ChildStopped(address, exception=exception))

    def force_stop(self):
        with suppress(Exception):
            self._process.on_stop()
