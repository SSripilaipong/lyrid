from dataclasses import dataclass

from lyrid.core.actor import IActorFactory
from lyrid.core.processor import Command


@dataclass
class SpawnActorCommand(Command):
    key: str
    type_: IActorFactory
