from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address


@dataclass(frozen=True)
class ChildStopped(Message):
    child_address: Address
    exception: Optional[Exception] = None


@dataclass(frozen=True)
class SupervisorForceStop(Message):
    address: Address
