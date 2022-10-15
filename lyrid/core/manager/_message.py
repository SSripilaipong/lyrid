from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Message, Address


@dataclass
class ManagerSpawnActorMessage(Message):
    address: Address
    type_: IActorFactory


@dataclass
class ManagerSpawnActorCompletedMessage(Message):
    actor_address: Address
    manager_address: Address
