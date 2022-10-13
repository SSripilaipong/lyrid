import multiprocessing as mp

from lyrid.base import ProcessorBase
from lyrid.core.processor import Command


def create_processor(*, command_queue: mp.Queue = None) -> ProcessorBase:
    command_queue = command_queue or mp.Queue()
    return ProcessorBase(handle=handle_mock, command_queue=command_queue)


def handle_mock(_: Command):
    pass
