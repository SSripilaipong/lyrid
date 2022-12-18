import queue

from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingToNodeCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.util.queue import iter_until_empty


def test_should_put_sending_to_node_command_to_command_queue_when_send_to_node_method_is_called():
    command_queue = queue.Queue()
    messenger = create_messenger(command_queue=command_queue)

    messenger.send_to_node(sender=Address("$.me"), of=Address("$.you"), message=MessageDummy("Hello"))

    assert list(iter_until_empty(command_queue)) == [SendingToNodeCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    )]
