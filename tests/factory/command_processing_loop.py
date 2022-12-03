import multiprocessing as mp
import queue
from typing import Callable

from lyrid.base import MultiProcessedCommandProcessingLoop
from lyrid.core.command_processing_loop import Command


def create_command_processing_loop(*, command_queue: queue.Queue = None,
                                   handle: Callable[[Command], None] = None) -> MultiProcessedCommandProcessingLoop:
    command_queue = command_queue or mp.Queue()
    handle = handle or handle_mock
    return MultiProcessedCommandProcessingLoop(handle=handle, command_queue=command_queue)


def handle_mock(_: Command):
    pass
