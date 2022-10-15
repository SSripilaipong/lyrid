from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@dataclass
class ActorMessageSendingCommand(Command):
    sender: Address
    receiver: Address
    message: Message


@dataclass
class SpawnActorCommand(Command):
    reply_to: Address
    address: Address
    type_: IActorFactory
