from lyrid.core.command_processing_loop import ProcessorStartCommand, ProcessorStopCommand
from tests.factory.messenger import create_messenger_command_processor


def test_should_handle_processor_start_command_safely():
    messenger = create_messenger_command_processor()

    messenger.handle_command(ProcessorStartCommand())


def test_should_handle_processor_stop_command_safely():
    messenger = create_messenger_command_processor()

    messenger.handle_command(ProcessorStopCommand())
