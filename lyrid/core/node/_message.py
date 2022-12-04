from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessFactory


@dataclass
class NodeSpawnProcessMessage(Message):
    address: Address
    type_: ProcessFactory
    ref_id: str
    initial_message: Optional[Message] = None


@dataclass
class NodeSpawnProcessCompletedMessage(Message):
    process_address: Address
    node_address: Address
    ref_id: str
