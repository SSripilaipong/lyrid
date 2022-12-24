from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address
from lyrid.core.process import Process


@dataclass
class NodeSpawnProcessMessage(Message):
    address: Address
    ref_id: str
    process: Process
    initial_message: Optional[Message] = None


@dataclass
class NodeSpawnProcessCompletedMessage(Message):
    process_address: Address
    node_address: Address
    ref_id: str
