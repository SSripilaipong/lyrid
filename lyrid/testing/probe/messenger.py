from dataclasses import dataclass
from typing import List, Callable, Any

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import Messenger


@dataclass
class SendEvent:
    sender: Address
    receiver: Address
    message: Message


class MessengerProbe(Messenger):

    def __init__(self):
        self._send__subscribers: List[Callable[[SendEvent], Any]] = []

    def send(self, sender: Address, receiver: Address, message: Message):
        for callback in self._send__subscribers:
            callback(SendEvent(sender, receiver, message))

    def send_to_node(self, sender: Address, of: Address, message: Message):
        pass

    def send__subscribe(self, callback: Callable[[SendEvent], Any]):
        self._send__subscribers.append(callback)
