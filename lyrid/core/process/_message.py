from dataclasses import dataclass

from lyrid.core.messaging import Message, Address


@dataclass
class ChildStopped(Message):
    child_address: Address


@dataclass(frozen=True)
class SupervisorForceStop(Message):
    address: Address


@dataclass
class WillForceStop(Message):
    pass
