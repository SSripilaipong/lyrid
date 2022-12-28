from dataclasses import dataclass

from ._message import Message, LyridMessage


@dataclass
class Ask(Message):
    message: Message
    ref_id: str


@dataclass
class Reply(LyridMessage):
    message: Message
    ref_id: str
