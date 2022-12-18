import queue

from lyrid.core.messaging import Address
from lyrid.core.messenger import (
    MessengerRegisterAddressMessage, RegisterAddressCommand, )
from tests.factory.messenger import create_messenger
from tests.util.queue import iter_until_empty


def test_should_pass_register_address_to_command_queue_when_sending_message_to_messenger_with_messenger_register_address_message():
    command_queue = queue.Queue()
    messenger = create_messenger(address=Address("#messenger"), command_queue=command_queue)

    messenger.send(
        sender=Address("$"),
        receiver=Address("#messenger"),
        message=MessengerRegisterAddressMessage(address=Address("$.new"), node_address=Address("#manager1"),
                                                ref_id="RefId123"),
    )

    assert list(iter_until_empty(command_queue)) == [RegisterAddressCommand(
        address=Address("$.new"), node_address=Address("#manager1"), requester_address=Address("$"),
        ref_id="RefId123",
    )]
