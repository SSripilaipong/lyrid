from dataclasses import dataclass
from typing import Optional

from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process


@dataclass
class SystemSpawnActorCommand(Command):
    key: str
    process: Process
    initial_message: Optional[Message] = None


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
