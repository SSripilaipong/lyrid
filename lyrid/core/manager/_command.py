from dataclasses import dataclass
from typing import Generic, TypeVar

from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessFactory
from lyrid.core.processor import Command

M = TypeVar("M", bound=Message)


@dataclass
class MessageHandlingCommand(Command, Generic[M]):
    sender: Address
    receiver: Address
    message: M


@dataclass
class SpawnActorCommand(Command):
    reply_to: Address
    address: Address
    type_: ProcessFactory
    ref_id: str
