from abc import abstractmethod
from typing import Protocol


class Randomizer(Protocol):

    @abstractmethod
    def randrange(self, n: int) -> int:
        pass
