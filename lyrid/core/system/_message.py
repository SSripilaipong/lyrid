from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address
from lyrid.core.process import Process


@dataclass
class SpawnChildMessage(Message):
    key: str
    process: Process
    initial_message: Optional[Message] = None


@dataclass
class SpawnChildCompleted(Message):
    key: str
    address: Address
