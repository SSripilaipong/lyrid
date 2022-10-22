from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass
class ChildActorTerminatedMessage(Message):
    child_address: Address
