import multiprocessing as mp
from dataclasses import dataclass

from lyrid.core.processor import Command
from tests.processor_factory import create_processor


def test_should_pass_command_to_handle_function():
    mp_manager = mp.Manager()
    handle_command = mp_manager.dict()

    def handle(command: Command):
        handle_command['value'] = command

    processor = create_processor(handle=handle)
    processor.start()

    processor.process(MyCommand("Hello"))

    assert handle_command.get('value') == MyCommand("Hello")


@dataclass
class MyCommand(Command):
    value: str
