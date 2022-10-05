from abc import abstractmethod
from typing import Protocol

from ._address import Address
from ._message import Message


class IReceiver(Protocol):

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass
