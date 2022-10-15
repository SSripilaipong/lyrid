from dataclasses import dataclass
from typing import Type

from lyrid.core.actor import IActor
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@dataclass
class ActorMessageSendingCommand(Command):
    sender: Address
    receiver: Address
    message: Message


@dataclass
class SpawnActorCommand(Command):
    address: Address
    type_: Type[IActor]
