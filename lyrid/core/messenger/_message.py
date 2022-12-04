from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass
class MessengerRegisterAddressMessage(Message):
    address: Address
    node_address: Address
    ref_id: str


@dataclass
class MessengerRegisterAddressCompletedMessage(Message):
    address: Address
    manager_address: Address
    ref_id: str
