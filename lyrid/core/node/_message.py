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
    actor_address: Address
    manager_address: Address
    ref_id: str
