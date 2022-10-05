from dataclasses import dataclass

from lyrid.core.messenger import Message


@dataclass(frozen=True)
class TextMessage(Message):
    text: str
