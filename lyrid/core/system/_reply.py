from dataclasses import dataclass

from lyrid.core.messaging import Address, Message


@dataclass
class SystemSpawnActorCompletedReply:
    address: Address


@dataclass
class ActorAskReply:
    address: Address
    message: Message
    ref_id: str
