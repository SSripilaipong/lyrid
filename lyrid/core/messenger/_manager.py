from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


class IManager(Protocol):

    @abstractmethod
    def handle_message(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def handle_processor_command(self, command: Command):
        pass
