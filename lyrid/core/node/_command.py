from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessFactory

M = TypeVar("M", bound=Message)


@dataclass
class MessageHandlingCommand(Command, Generic[M]):
    sender: Address
    receiver: Address
    message: M


@dataclass
class SpawnProcessCommand(Command):
    reply_to: Address
    address: Address
    type_: ProcessFactory
    ref_id: str
    initial_message: Optional[Message] = None
