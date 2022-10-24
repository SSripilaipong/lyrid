from abc import abstractmethod
from typing import Protocol


class IIdGenerator(Protocol):

    @abstractmethod
    def generate(self) -> str:
        pass
