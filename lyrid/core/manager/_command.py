from dataclasses import dataclass

from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


@dataclass
class ActorMessageSendingCommand(Command):
    sender: Address
    receiver: Address
    message: Message
