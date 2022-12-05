from abc import ABC, abstractmethod
from contextlib import suppress
from enum import Enum
from typing import TypeVar, Set, Optional, Callable, Tuple, SupportsFloat

from lyrid.core.actor import BackgroundTaskExecutor
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.process import ProcessFactory, Process, ProcessStoppedSignal, ChildStopped, SupervisorForceStop
from lyrid.core.system import SpawnChildMessage
from ._background_task_executor import ThreadBackgroundTaskExecutor

T = TypeVar("T", bound='Actor')


class ActorStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    STOPPING: str = "STOPPING"


class Actor(Process, ABC):

    def __init__(self, address: Address, messenger: IMessenger,
                 background_task_executor: BackgroundTaskExecutor = None):
        self._address = address
        self._messenger = messenger
        self._system_address = Address("$")
        self._background_task_executor = background_task_executor or ThreadBackgroundTaskExecutor()

        self._status = ActorStatus.ACTIVE
        self._active_children: Set[Address] = set()
        self._stopped_message_to_report: Optional[ChildStopped] = None

    @property
    def address(self) -> Address:
        return self._address

    def tell(self, receiver: Address, message: Message, *, delay: SupportsFloat = None):
        if delay is None:
            self._messenger.send(self._address, receiver, message)
        else:
            self._background_task_executor.execute_with_delay(self._messenger.send, delay=delay,
                                                              args=(self._address, receiver, message))

    def spawn(self, key: str, type_: ProcessFactory, *, initial_message: Optional[Message] = None):
        self._messenger.send(self._address, self._system_address,
                             SpawnChildMessage(key=key, type_=type_, initial_message=initial_message))
        self._active_children.add(self._address.child(key))

    def run_in_background(self, task: Callable, *, args: Tuple = ()):
        self._background_task_executor.execute(task, args=args)

    def receive(self, sender: Address, message: Message):
        if isinstance(message, ChildStopped):
            self._active_children -= {message.child_address}
        elif isinstance(message, SupervisorForceStop):
            self._handle_stopping(None)

        if self._status is ActorStatus.ACTIVE:
            self._receive_when_active(sender, message)
        elif self._status is ActorStatus.STOPPING:
            self._receive_when_stopping(sender, message)

    def stop(self):
        raise ProcessStoppedSignal()

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass

    def on_stop(self):
        pass

    def _receive_when_active(self, sender: Address, message: Message):
        try:
            self.on_receive(sender, message)
        except ProcessStoppedSignal:
            self._handle_stopping(None)
        except Exception as e:
            self._handle_stopping(e)

    def _handle_stopping(self, exception: Exception = None):
        with suppress(Exception):
            self.on_stop()
        self._status = ActorStatus.STOPPING
        self._stopped_message_to_report = ChildStopped(child_address=self._address, exception=exception)
        if not self._active_children:
            self.tell(self._address.supervisor(), self._stopped_message_to_report)
            raise ProcessStoppedSignal()
        else:
            for child in self._active_children:
                self.tell(child, SupervisorForceStop(address=child))

    def _receive_when_stopping(self, _: Address, __: Message):
        if not self._active_children:
            if self._stopped_message_to_report is not None:
                self.tell(self._address.supervisor(), self._stopped_message_to_report)
            raise ProcessStoppedSignal()
