from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IManager
from lyrid.core.processor import Command


class MessengerMock:

    def __init__(self):
        self.send__sender = None
        self.send__receiver = None
        self.send__message = None

    def send(self, sender: Address, receiver: Address, message: Message):
        self.send__sender = sender
        self.send__receiver = receiver
        self.send__message = message

    def handle_processor_command(self, command: Command):
        pass

    def add_manager(self, address: Address, manager: IManager):
        pass

    def initial_register_address(self, actor_address: Address, manager_address: Address):
        pass
