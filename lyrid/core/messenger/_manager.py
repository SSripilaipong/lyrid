from abc import abstractmethod
from typing import Protocol, runtime_checkable

from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@runtime_checkable
class IManager(Protocol):

    @abstractmethod
    def handle_message(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def handle_processor_command(self, command: Command):
        pass
