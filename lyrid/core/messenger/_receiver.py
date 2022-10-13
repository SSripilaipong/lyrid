from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message


class IReceiver(Protocol):

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass
