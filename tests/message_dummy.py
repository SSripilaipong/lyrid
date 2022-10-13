from dataclasses import dataclass

from lyrid.core.messaging import Message


@dataclass(frozen=True)
class MessageDummy(Message):
    text: str
