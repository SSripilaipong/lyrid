from dataclasses import dataclass
from typing import Type

from lyrid.core.actor import IActor
from lyrid.core.processor import Command


@dataclass
class SpawnActorCommand(Command):
    key: str
    type_: Type[IActor]
