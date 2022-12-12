import multiprocessing as mp
import queue
from typing import Callable, Optional

from lyrid.core.command_processing_loop import Command, CommandProcessingLoop, ProcessorStopCommand, \
    ProcessorStartCommand

HandleFunc = Callable[[Command], None]


class MultiProcessedCommandProcessingLoop(CommandProcessingLoop):
    def __init__(self, command_queue: queue.Queue, handle: HandleFunc = None):
        self._handle = handle
        self._command_queue = command_queue

        self._process: Optional[mp.Process] = None

    def set_handle(self, handle: HandleFunc):
        self._handle = handle

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
