from abc import abstractmethod
from typing import Protocol

from ._command import Command


class CommandProcessingLoop(Protocol):

    @abstractmethod
    def process(self, command: Command):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
