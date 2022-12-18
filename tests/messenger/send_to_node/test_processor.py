from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingToNodeCommand, RegisterAddressCommand
from tests.factory.messenger import create_messenger_command_processor
from tests.message_dummy import MessageDummy
from tests.mock.node import NodeMock


def test_should_pass_message_to_the_node_of_the_registered_address_when_handling_sending_to_node_command():
    node = NodeMock()
    messenger = create_messenger_command_processor(nodes={
        Address("#node1"): NodeMock(),
        Address("#node2"): node,
        Address("#node3"): NodeMock(),
    })
    messenger.handle_command(RegisterAddressCommand(
        address=Address("$.you"),
        node_address=Address("#node2"),
        requester_address=Address("$"),
        ref_id="...",
    ))

    messenger.handle_command(SendingToNodeCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert node.handle_message__sender == Address("$.me") and \
           node.handle_message__receiver == Address("#node2") and \
           node.handle_message__message == MessageDummy("Hello")
