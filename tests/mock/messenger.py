from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import Node, Messenger


class MessengerMock(Messenger):

    def __init__(self):
        self.send__sender = None
        self.send__receiver = None
        self.send__message = None

        self.send__senders = []
        self.send__receivers = []
        self.send__messages = []

        self.send_to_node__senders = []
        self.send_to_node__ofs = []
        self.send_to_node__messages = []

    def send(self, sender: Address, receiver: Address, message: Message):
        self.send__sender = sender
        self.send__receiver = receiver
        self.send__message = message

        self.send__senders.append(sender)
        self.send__receivers.append(receiver)
        self.send__messages.append(message)

    def send_to_node(self, sender: Address, of: Address, message: Message):
        self.send_to_node__senders.append(sender)
        self.send_to_node__ofs.append(of)
        self.send_to_node__messages.append(message)

    def handle_processor_command(self, command: Command):
        pass

    def add_node(self, address: Address, node: Node):
        pass

    def initial_register_address(self, actor_address: Address, node_address: Address):
        pass

    def send__clear_captures(self):
        self.send__sender = None
        self.send__receiver = None
        self.send__message = None

        self.send__senders = []
        self.send__receivers = []
        self.send__messages = []
