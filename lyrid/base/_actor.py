from abc import ABC, abstractmethod
from typing import TypeVar

from lyrid.core.actor import IActorFactory, IActor, ActorStoppedSignal, ChildActorStopped
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.system import SpawnChildMessage

T = TypeVar("T", bound='ActorBase')


class ActorBase(IActor, ABC):

    def __init__(self, address: Address, messenger: IMessenger):
        self._address = address
        self._messenger = messenger
        self._system_address = Address("$")

    def tell(self, receiver: Address, message: Message):
        self._messenger.send(self._address, receiver, message)

    def spawn(self, key: str, type_: 'IActorFactory'):
        self._messenger.send(self._address, self._system_address, SpawnChildMessage(key=key, type_=type_))

    def receive(self, sender: Address, message: Message):
        try:
            self.on_receive(sender, message)
        except ActorStoppedSignal as s:
            self.tell(self._address.supervisor(), ChildActorStopped(child_address=self._address))
            raise s

    def stop(self):
        raise ActorStoppedSignal()

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass
