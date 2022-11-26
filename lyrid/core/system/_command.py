from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@dataclass
class SystemSpawnActorCommand(Command):
    key: str
    type_: IActorFactory


@dataclass
class SystemAskCommand(Command):
    address: Address
    message: Message
    ref_id: str


@dataclass
class ActorReplyAskCommand(Command):
    address: Address
    message: Message
    ref_id: str
