from lyrid.core.messenger import Address, Message


class ManagerMock:
    def __init__(self):
        self.handle_sender = None
        self.handle_receiver = None
        self.handle_message = None

    def handle(self, sender: Address, receiver: Address, message: Message):
        self.handle_sender = sender
        self.handle_receiver = receiver
        self.handle_message = message
