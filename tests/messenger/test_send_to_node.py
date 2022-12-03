from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingToManagerCommand, RegisterAddressCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.mock.node import NodeMock
from tests.mock.processor import ProcessorMock


def test_should_pass_sending_to_node_command_to_processor_when_send_to_node_method_is_called():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send_to_node(sender=Address("$.me"), of=Address("$.you"), message=MessageDummy("Hello"))

    assert processor.process__command == SendingToManagerCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    )


def test_should_let_node_of_the_registered_address_handle_the_message_to_itself_when_handling_sending_to_node_command():
    # noinspection DuplicatedCode
    node = NodeMock()
    messenger = create_messenger(nodes={
        Address("#node1"): NodeMock(),
        Address("#node2"): node,
        Address("#node3"): NodeMock(),
    })
    messenger.handle_processor_command(RegisterAddressCommand(
        address=Address("$.you"),
        node_address=Address("#node2"),
        requester_address=Address("$"),
        ref_id="...",
    ))

    messenger.handle_processor_command(SendingToManagerCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert node.handle_message__sender == Address("$.me") and \
           node.handle_message__receiver == Address("#node2") and \
           node.handle_message__message == MessageDummy("Hello")
