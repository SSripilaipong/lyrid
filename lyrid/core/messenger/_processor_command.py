from dataclasses import dataclass

from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message


@dataclass
class SendingCommand(Command):
    sender: Address
    receiver: Address
    message: Message


@dataclass
class SendingToManagerCommand(Command):
    sender: Address
    of: Address
    message: Message


@dataclass
class RegisterAddressCommand(Command):
    address: Address
    node_address: Address
    requester_address: Address
    ref_id: str
