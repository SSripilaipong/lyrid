import multiprocessing as mp
from dataclasses import dataclass

from lyrid.core.command_processing_loop import ProcessorStopCommand, Command, ProcessorStartCommand
from tests.factory.command_processing_loop import create_command_processing_loop


def test_should_stop_processor():
    processor = create_command_processing_loop()
    processor.start()
    processor.stop()


def test_should_stop_processor_loop_by_processor_stop_command():
    command_queue = mp.Queue()
    command_queue.put(ProcessorStopCommand())
    processor = create_command_processing_loop(command_queue=command_queue)
    processor.processor_loop()


def test_should_pass_processor_start_and_stop_command_to_handle_when_started_and_stopping():
    commands = []

    def handle(command: Command):
        commands.append(command)

    command_queue = mp.Queue()
    command_queue.put(ProcessorStopCommand())

    processor = create_command_processing_loop(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert commands == [ProcessorStartCommand(), ProcessorStopCommand()]


def test_should_pass_non_processor_command_to_handle():
    commands = []

    def handle(command: Command):
        commands.append(command)

    command_queue = mp.Queue()
    command_queue.put(MyCommand("Hello"))
    command_queue.put(ProcessorStopCommand())

    processor = create_command_processing_loop(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert commands == [ProcessorStartCommand(), MyCommand("Hello"), ProcessorStopCommand()]


def test_should_handle_multiple_commands():
    commands = []

    def handle(command: Command):
        commands.append(command)

    command_queue = mp.Queue()
    command_queue.put(MyCommand("Hello1"))
    command_queue.put(MyCommand("Hello2"))
    command_queue.put(ProcessorStopCommand())

    processor = create_command_processing_loop(command_queue=command_queue, handle=handle)
    processor.processor_loop()

    assert commands == [ProcessorStartCommand(), MyCommand("Hello1"), MyCommand("Hello2"), ProcessorStopCommand()]


@dataclass
class MyCommand:
    value: str
