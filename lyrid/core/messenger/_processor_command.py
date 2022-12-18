from dataclasses import dataclass

from lyrid.core.command_processing_loop import Command
from lyrid.core.messaging import Address, Message


class MessengerCommand(Command):
    pass


@dataclass
class SendingCommand(MessengerCommand):
    sender: Address
    receiver: Address
    message: Message


@dataclass
class SendingToNodeCommand(MessengerCommand):
    sender: Address
    of: Address
    message: Message


@dataclass
class RegisterAddressCommand(MessengerCommand):
    address: Address
    node_address: Address
    requester_address: Address
    ref_id: str
