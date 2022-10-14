from dataclasses import dataclass

from lyrid.core.actor import IActor
from lyrid.core.messaging import Message, Address


@dataclass
class ManagerSpawnActorCommand(Message):
    address: Address
    type_: IActor
