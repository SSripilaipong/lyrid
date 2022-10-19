from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Address
from lyrid.core.processor import Command


@dataclass
class SystemSpawnActorCommand(Command):
    key: str
    type_: IActorFactory


@dataclass
class AcknowledgeManagerSpawnActorCompletedCommand(Command):
    actor_address: Address
    manager_address: Address


@dataclass
class AcknowledgeMessengerRegisterAddressCompletedCommand(Command):
    actor_address: Address
    manager_address: Address
