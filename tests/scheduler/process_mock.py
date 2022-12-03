from typing import Optional, List

from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessStoppedSignal, Process


class MyProcess(Process):
    def __init__(self):
        self.receive__sender: Optional[Address] = None
        self.receive__message: Optional[Message] = None
        self.receive__senders: List[Address] = []
        self.receive__messages: List[Message] = []

    def receive(self, sender: Address, message: Message):
        self.receive__sender = sender
        self.receive__message = message
        self.receive__senders.append(sender)
        self.receive__messages.append(message)


class WillStop(Process):
    def __init__(self):
        self.receive__senders: List[Address] = []
        self.receive__messages: List[Message] = []

    def receive(self, sender: Address, message: Message):
        self.receive__senders.append(sender)
        self.receive__messages.append(message)
        raise ProcessStoppedSignal()
