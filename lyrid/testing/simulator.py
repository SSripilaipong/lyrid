import uuid
from contextlib import suppress
from typing import Any

from lyrid import Ask, BackgroundTaskExited
from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessStoppedSignal
from .background_task import BackgroundTask
from .captor import Captor


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

    def background_task_exit(self, task_id: str, *, return_value: Any = None):
        self._process.receive(self._actor_address, BackgroundTaskExited(task_id, return_value=return_value))
