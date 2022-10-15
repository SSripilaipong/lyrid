from abc import ABC, abstractmethod
from typing import TypeVar

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger

T = TypeVar("T", bound='ActorBase')


class ActorBase(ABC):

    def __init__(self, address: Address, messenger: IMessenger):
        self._address = address
        self._messenger = messenger

    def tell(self, receiver: Address, message: Message):
        self._messenger.send(self._address, receiver, message)

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass
