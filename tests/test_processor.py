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
    commands = []

    def handle(command: Command):
        commands.append(command)

    command_queue = mp.Queue()
    command_queue.put(MyCommand("Hello"))
    command_queue.put(ProcessorStopCommand())

    processor = create_processor(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert commands == [MyCommand("Hello")]


def test_should_handle_multiple_commands():
    commands = []

    def handle(command: Command):
        commands.append(command)

    command_queue = mp.Queue()
    command_queue.put(MyCommand("Hello1"))
    command_queue.put(MyCommand("Hello2"))
    command_queue.put(ProcessorStopCommand())

    processor = create_processor(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert commands == [MyCommand("Hello1"), MyCommand("Hello2")]


@dataclass
class MyCommand:
    value: str
