from abc import abstractmethod
from typing import Protocol

from ._command import Command


class IProcessor(Protocol):

    @abstractmethod
    def process(self, command: Command):
        pass
