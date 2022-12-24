from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessFactory, Process


@dataclass
class SpawnChildMessage(Message):
    key: str
    type_: ProcessFactory
    process: Optional[Process]
    initial_message: Optional[Message] = None


@dataclass
class SpawnChildCompleted(Message):
    key: str
    address: Address
