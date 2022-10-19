import multiprocessing as mp
import queue
from typing import Callable

from lyrid.base import ProcessorBase
from lyrid.core.processor import Command


def create_processor(*, command_queue: queue.Queue = None, handle: Callable[[Command], None] = None) -> ProcessorBase:
    command_queue = command_queue or mp.Queue()
    handle = handle or handle_mock
    return ProcessorBase(handle=handle, command_queue=command_queue)


def handle_mock(_: Command):
    pass
