from dataclasses import dataclass

from lyrid.core.messenger import Address, Message
from lyrid.core.processor import Command


@dataclass
class SendingCommand(Command):
    sender: Address
    receiver: Address
    message: Message


@dataclass
class RegisterAddressCommand(Command):
    addr: Address
    manager_key: str
