from abc import ABC, abstractmethod
from typing import TypeVar

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.system import ActorSpawnChildActorMessage

T = TypeVar("T", bound='ActorBase')


class ActorBase(ABC):

    def __init__(self, address: Address, messenger: IMessenger):
        self._address = address
        self._messenger = messenger
        self._system_address = Address("$")

    def tell(self, receiver: Address, message: Message):
        self._messenger.send(self._address, receiver, message)

    def spawn(self, key: str, type_: 'IActorFactory'):
        self._messenger.send(self._address, self._system_address, ActorSpawnChildActorMessage(key=key, type_=type_))

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass
