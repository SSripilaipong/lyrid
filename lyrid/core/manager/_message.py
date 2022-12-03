from dataclasses import dataclass

from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessFactory


@dataclass
class ManagerSpawnActorMessage(Message):
    address: Address
    type_: ProcessFactory
    ref_id: str


@dataclass
class ManagerSpawnActorCompletedMessage(Message):
    actor_address: Address
    manager_address: Address
    ref_id: str
