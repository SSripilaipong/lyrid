import multiprocessing as mp
from typing import Callable, Optional

from lyrid.core.processor import Command, IProcessor, ProcessorStopCommand, ProcessorStartCommand


class ProcessorBase(IProcessor):
    def __init__(self, handle: Callable[[Command], None], command_queue: mp.Queue):
        self._handle = handle
        self._command_queue = command_queue

        self._process: Optional[mp.Process] = None

    def process(self, command: Command):
        self._command_queue.put(command)

    def start(self):
        self._process = mp.Process(target=self.processor_loop)
        self._process.start()

    def processor_loop(self):
        self._handle(ProcessorStartCommand())
        while True:
            command: Command = self._command_queue.get(block=True)
            self._handle(command)
            if isinstance(command, ProcessorStopCommand):
                break

    def stop(self):
        self.process(ProcessorStopCommand())
        self._process.join()
