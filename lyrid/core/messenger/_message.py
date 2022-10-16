from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass
class MessengerRegisterAddressMessage(Message):
    address: Address
    manager: Address
