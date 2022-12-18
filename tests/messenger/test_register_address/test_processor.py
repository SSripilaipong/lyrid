import queue

from lyrid.core.messaging import Address
from lyrid.core.messenger import (
    RegisterAddressCommand, SendingCommand, MessengerRegisterAddressCompletedMessage,
)
from tests.factory.messenger import create_messenger_command_processor
from tests.mock.node import NodeMock
from tests.util.queue import iter_until_empty


def test_should_put_sending_command_of_the_reply_message_to_command_queue_when_handle_register_address_command():
    command_queue = queue.Queue()
    messenger = create_messenger_command_processor(
        address=Address("#messenger"), command_queue=command_queue, nodes={Address("#manager1"): NodeMock()},
    )

    messenger.handle_command(RegisterAddressCommand(
        address=Address("$.new"),
        node_address=Address("#manager1"),
        requester_address=Address("$"),
        ref_id="RefId999",
    ))

    assert list(iter_until_empty(command_queue)) == [SendingCommand(
        sender=Address("#messenger"),
        receiver=Address("$"),
        message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.new"),
            manager_address=Address("#manager1"),
            ref_id="RefId999",
        ),
    )]
