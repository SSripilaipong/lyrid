from dataclasses import dataclass
from typing import Optional

from lyrid.core.messaging import Message, Address, LyridMessage


@dataclass(frozen=True)
class ChildStopped(LyridMessage):
    child_address: Address
    exception: Optional[Exception] = None


@dataclass(frozen=True)
class SupervisorForceStop(Message):
    address: Address
