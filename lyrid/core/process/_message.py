from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass(frozen=True)
class ChildStopped(Message):
    child_address: Address


@dataclass(frozen=True)
class SupervisorForceStop(Message):
    address: Address
