from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message
from . import IManager
from ..processor import Command


class IMessenger(Protocol):

    @abstractmethod
    def send(self, sender: Address, receiver: Address, message: Message):
        pass

    @abstractmethod
    def send_to_manager(self, sender: Address, of: Address, message: Message):
        pass

    @abstractmethod
    def handle_processor_command(self, command: Command):
        pass

    @abstractmethod
    def add_manager(self, address: Address, manager: IManager):
        pass

    @abstractmethod
    def initial_register_address(self, actor_address: Address, manager_address: Address):
        pass
