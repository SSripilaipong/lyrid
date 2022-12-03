from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message
from ._node import Node
from ..command_processing_loop import Command


class IMessenger(Protocol):

    @abstractmethod
    def send(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def send_to_node(self, sender: Address, of: Address, message: Message):
        pass

    @abstractmethod
    def handle_processor_command(self, command: Command):
        pass

    @abstractmethod
    def add_node(self, address: Address, node: Node):
        pass

    @abstractmethod
    def initial_register_address(self, actor_address: Address, node_address: Address):
        pass
