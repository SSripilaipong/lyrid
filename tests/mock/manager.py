from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


class ManagerMock:
    def __init__(self):
        self.handle_message__sender = None
        self.handle_message__receiver = None
        self.handle_message__message = None

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        self.handle_message__sender = sender
        self.handle_message__receiver = receiver
        self.handle_message__message = message

    def handle_processor_command(self, command: Command):
        pass
