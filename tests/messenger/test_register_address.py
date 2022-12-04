from lyrid.core.messaging import Address
from lyrid.core.messenger import (
    MessengerRegisterAddressMessage, RegisterAddressCommand, SendingCommand, MessengerRegisterAddressCompletedMessage,
)
from tests.factory.messenger import create_messenger
from tests.mock.node import NodeMock
from tests.mock.processor import ProcessorMock


def test_should_pass_register_address_to_processor_when_sending_message_to_messenger_with_messenger_register_address_message():
    processor = ProcessorMock()
    messenger = create_messenger(address=Address("#messenger"), processor=processor)

    messenger.send(
        sender=Address("$"),
        receiver=Address("#messenger"),
        message=MessengerRegisterAddressMessage(address=Address("$.new"), node_address=Address("#manager1"),
                                                ref_id="RefId123"),
    )

    assert processor.process__command == RegisterAddressCommand(
        address=Address("$.new"), node_address=Address("#manager1"), requester_address=Address("$"),
        ref_id="RefId123",
    )


def test_should_let_processor_process_sending_command_of_the_reply_message_when_handle_register_address_command():
    processor = ProcessorMock()
    messenger = create_messenger(
        address=Address("#messenger"), processor=processor, nodes={Address("#manager1"): NodeMock()},
    )

    messenger.handle_processor_command(RegisterAddressCommand(
        address=Address("$.new"),
        node_address=Address("#manager1"),
        requester_address=Address("$"),
        ref_id="RefId999",
    ))

    assert processor.process__command == SendingCommand(
        sender=Address("#messenger"),
        receiver=Address("$"),
        message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.new"),
            manager_address=Address("#manager1"),
            ref_id="RefId999",
        ),
    )
