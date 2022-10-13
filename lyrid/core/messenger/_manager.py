from abc import abstractmethod
from typing import Protocol

from ._address import Address
from ._message import Message


class IManager(Protocol):

    @abstractmethod
    def handle(self, sender: Address, receiver: Address, message: Message):
        pass
