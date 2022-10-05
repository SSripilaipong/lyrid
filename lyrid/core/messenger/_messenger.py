from abc import abstractmethod
from typing import Protocol

from ._address import Address
from ._message import Message


class IMessenger(Protocol):

    @abstractmethod
    def send(self, sender: Address, receiver: Address, message: Message):
        pass
