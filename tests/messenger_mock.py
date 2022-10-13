from lyrid.core.messaging import Address, Message
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
