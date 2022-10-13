import multiprocessing as mp
from dataclasses import dataclass

from lyrid.core.processor import ProcessorStopCommand, Command
from tests.processor_factory import create_processor


def test_should_stop_processor():
    processor = create_processor()
    processor.start()
    processor.stop()


def test_should_stop_processor_loop_by_processor_stop_command():
    command_queue = mp.Queue()
    command_queue.put(ProcessorStopCommand())
    processor = create_processor(command_queue=command_queue)
    processor.processor_loop()


def test_should_pass_non_processor_command_to_handle():
    def handle(command: Command):
        handle.command = command

    handle.command = None

    command_queue = mp.Queue()
    command_queue.put(MyCommand("Hello"))
    command_queue.put(ProcessorStopCommand())

    processor = create_processor(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert handle.command == MyCommand("Hello")


@dataclass
class MyCommand:
    value: str
