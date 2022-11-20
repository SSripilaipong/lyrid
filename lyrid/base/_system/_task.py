from abc import ABC
from dataclasses import dataclass

from lyrid.core.messaging import Address


class Task(ABC):
    pass


@dataclass
class ActorSpawnChildTask(Task):
    requester: Address
    child_key: str
