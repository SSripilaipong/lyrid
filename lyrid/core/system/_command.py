from dataclasses import dataclass
from typing import Type

from lyrid.core.actor import IActor
from lyrid.core.messaging import Message, Address


@dataclass
class ManagerSpawnActorCommand(Message):
    address: Address
    type_: Type[IActor]
