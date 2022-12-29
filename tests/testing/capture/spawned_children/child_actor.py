from dataclasses import dataclass

from lyrid import Actor


@dataclass(frozen=True)
class ChildActor(Actor):
    name: str
    value: int
