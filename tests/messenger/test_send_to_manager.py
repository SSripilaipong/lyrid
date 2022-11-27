from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingToManagerCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.mock.processor import ProcessorMock


def test_should_pass_sending_to_manager_command_to_processor_when_send_to_manager_method_is_called():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send_to_manager(sender=Address("$.me"), of=Address("$.you"), message=MessageDummy("Hello"))

    assert processor.process__command == SendingToManagerCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    )
