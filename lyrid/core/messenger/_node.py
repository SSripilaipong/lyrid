from abc import abstractmethod
from typing import Protocol, runtime_checkable

from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message


@runtime_checkable
class Node(Protocol):

    @abstractmethod
    def handle_message(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def handle_processor_command(self, command: Command):
        pass
