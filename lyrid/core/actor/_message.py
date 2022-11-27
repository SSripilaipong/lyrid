from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass
class ChildActorStopped(Message):
    child_address: Address
