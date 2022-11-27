from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IManager, IMessenger
from lyrid.core.processor import Command


class MessengerMock(IMessenger):

    def __init__(self):
        self.send__sender = None
        self.send__receiver = None
        self.send__message = None

        self.send_to_manager__senders = []
        self.send_to_manager__ofs = []
        self.send_to_manager__messages = []

    def send(self, sender: Address, receiver: Address, message: Message):
        self.send__sender = sender
        self.send__receiver = receiver
        self.send__message = message

    def send_to_manager(self, sender: Address, of: Address, message: Message):
        self.send_to_manager__senders.append(sender)
        self.send_to_manager__ofs.append(of)
        self.send_to_manager__messages.append(message)

    def handle_processor_command(self, command: Command):
        pass

    def add_manager(self, address: Address, manager: IManager):
        pass

    def initial_register_address(self, actor_address: Address, manager_address: Address):
        pass
