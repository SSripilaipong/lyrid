from typing import List

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import Messenger


class MessengerForTesting(Messenger):

    def __init__(self):
        self.send__receivers: List[Address] = []
        self.send__messages: List[Message] = []

    def send(self, sender: Address, receiver: Address, message: Message):
        self.send__receivers.append(receiver)
        self.send__messages.append(message)

    def send_to_node(self, sender: Address, of: Address, message: Message):
        pass
