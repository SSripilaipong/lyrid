import queue

from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.util.queue import iter_until_empty


def test_should_pass_sending_command_to_command_queue_when_send_method_is_called():
    command_queue = queue.Queue()
    messenger = create_messenger(command_queue=command_queue)

    messenger.send(Address("$.me"), Address("$.you"), MessageDummy("Hello"))

    assert list(iter_until_empty(command_queue)) == [SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    )]
