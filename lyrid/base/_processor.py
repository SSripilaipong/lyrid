from typing import Callable

from lyrid.core.processor import Command, IProcessor


class ProcessorBase(IProcessor):
    def __init__(self, handle: Callable[[Command], None]):
        self._handle = handle

    def process(self, command: Command):
        self._handle(command)

    def start(self):
        pass
