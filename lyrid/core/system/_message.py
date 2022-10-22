from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.messaging import Message


@dataclass
class ActorSpawnChildActorMessage(Message):
    key: str
    type_: IActorFactory
