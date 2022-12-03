from lyrid.core.command_processing_loop import ProcessorStartCommand, ProcessorStopCommand
from tests.factory.messenger import create_messenger


def test_should_receive_processor_start_command_safely():
    messenger = create_messenger()

    messenger.handle_processor_command(ProcessorStartCommand())


def test_should_receive_processor_stop_command_safely():
    messenger = create_messenger()

    messenger.handle_processor_command(ProcessorStopCommand())
