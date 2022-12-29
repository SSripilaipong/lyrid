from dataclasses import dataclass
from typing import Optional, SupportsFloat

from lyrid.base.actor import AbstractActor
from lyrid.core.messaging import Address, Message


@dataclass(frozen=True)
class CapturedMessage:
    receiver: Address
    message: Message
    delay: Optional[SupportsFloat] = None


@dataclass(frozen=True)
class CapturedSpawnedChild:
    actor: AbstractActor
    address: Address
    initial_message: Optional[Message] = None
