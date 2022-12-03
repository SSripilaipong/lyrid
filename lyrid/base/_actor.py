from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Set

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.process import ProcessFactory, Process, ProcessStoppedSignal, ChildStopped, SupervisorForceStop
from lyrid.core.system import SpawnChildMessage

T = TypeVar("T", bound='ActorBase')


class ActorStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    STOPPING: str = "STOPPING"


class ActorBase(Process, ABC):

    def __init__(self, address: Address, messenger: IMessenger):
        self._address = address
        self._messenger = messenger
        self._system_address = Address("$")

        self._status = ActorStatus.ACTIVE
        self._active_children: Set[Address] = set()

    def tell(self, receiver: Address, message: Message):
        self._messenger.send(self._address, receiver, message)

    def spawn(self, key: str, type_: 'ProcessFactory'):
        self._messenger.send(self._address, self._system_address, SpawnChildMessage(key=key, type_=type_))
        self._active_children.add(self._address.child(key))

    def receive(self, sender: Address, message: Message):
        if isinstance(message, ChildStopped):
            self._active_children -= {message.child_address}

        if self._status is ActorStatus.ACTIVE:
            self._receive_when_active(sender, message)
        elif self._status is ActorStatus.STOPPING:
            self._receive_when_stopping(sender, message)

    def stop(self):
        raise ProcessStoppedSignal()

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass

    def _receive_when_active(self, sender: Address, message: Message):
        try:
            self.on_receive(sender, message)
        except ProcessStoppedSignal as s:
            self._status = ActorStatus.STOPPING
            self.tell(self._address.supervisor(), ChildStopped(child_address=self._address))

            if not self._active_children:
                raise s
            else:
                for child in self._active_children:
                    self._messenger.send_to_manager(self._address, of=child,
                                                    message=SupervisorForceStop(address=child))

    def _receive_when_stopping(self, _: Address, __: Message):
        if not self._active_children:
            raise ProcessStoppedSignal()
