from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@dataclass
class SystemSpawnActorCommand(Command):
    key: str
    type_: IActorFactory


@dataclass
class AcknowledgeManagerSpawnActorCompletedCommand(Command):
    actor_address: Address
    manager_address: Address
    ref_id: str


@dataclass
class AcknowledgeMessengerRegisterAddressCompletedCommand(Command):
    actor_address: Address
    manager_address: Address
    ref_id: str


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


@dataclass
class ActorSpawnChildActorCommand(Command):
    actor_address: Address
    child_key: str
    child_type: IActorFactory
