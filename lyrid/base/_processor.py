import multiprocessing as mp
from typing import Callable, Optional

from lyrid.core.processor import Command, IProcessor, ProcessorStopCommand


class ProcessorBase(IProcessor):
    def __init__(self, handle: Callable[[Command], None]):
        self._handle = handle
        self._command_queue = mp.Queue()

        self._process: Optional[mp.Process] = None

    def process(self, command: Command):
        self._command_queue.put(command)

    def start(self):
        self._process = mp.Process(target=self._processor_loop)
        self._process.start()

    def _processor_loop(self):
        command: Command = self._command_queue.get(block=True)
        self._handle(command)

    def stop(self):
        self.process(ProcessorStopCommand())
        self._process.join()
