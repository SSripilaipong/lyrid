from dataclasses import dataclass

from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessFactory


@dataclass
class SpawnChildMessage(Message):
    key: str
    type_: ProcessFactory


@dataclass
class SpawnChildCompletedMessage(Message):
    key: str
    address: Address
