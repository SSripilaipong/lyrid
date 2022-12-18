from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message


class Messenger(Protocol):

    @abstractmethod
    def send(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def send_to_node(self, sender: Address, of: Address, message: Message):
        pass
