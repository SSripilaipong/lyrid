from dataclasses import dataclass
from typing import Optional, SupportsFloat, List

from lyrid.core.messaging import Address, Message
from .mock import MessengerForTesting


@dataclass
class CapturedMessage:
    receiver: Address
    message: Message
    delay: Optional[SupportsFloat] = None


class Captor:
    def __init__(self, messenger: MessengerForTesting):
        self._messenger = messenger

    def get_told_messages(self) -> List[CapturedMessage]:
        receivers = self._messenger.send__receivers
        messages = self._messenger.send__messages

        return [CapturedMessage(receiver, message, delay=None) for receiver, message in zip(receivers, messages)]
