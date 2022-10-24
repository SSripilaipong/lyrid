from dataclasses import dataclass

from ._message import Message


@dataclass
class Ask(Message):
    message: Message
    ref_id: str


@dataclass
class Reply(Message):
    message: Message
    ref_id: str
