from dataclasses import dataclass

from lyrid.core.messaging import Address


@dataclass
class SystemSpawnActorCompletedReply:
    address: Address
