from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressMessage, RegisterAddressCommand
from tests.factory.messenger import create_messenger
from tests.mock.processor import ProcessorMock


def test_should_pass_register_address_to_processor_when_sending_message_to_messenger_with_messenger_register_address_message():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send(
        sender=Address("$"),
        receiver=Address("#messenger"),
        message=MessengerRegisterAddressMessage(address=Address("$.new"), manager_address=Address("#manager1")),
    )

    assert processor.process__command == RegisterAddressCommand(
        address=Address("$.new"), manager_address=Address("#manager1"), requester_address=Address("$"),
    )
