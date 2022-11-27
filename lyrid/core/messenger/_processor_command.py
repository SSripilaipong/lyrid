from dataclasses import dataclass

from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


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
    manager_address: Address
    requester_address: Address
    ref_id: str
