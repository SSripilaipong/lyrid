from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Message, Address


@dataclass
class SpawnChildMessage(Message):
    key: str
    type_: IActorFactory


@dataclass
class SpawnChildCompletedMessage(Message):
    key: str
    address: Address
