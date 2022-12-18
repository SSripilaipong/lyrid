from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingCommand, RegisterAddressCommand
from tests.factory.messenger import create_messenger_command_processor
from tests.message_dummy import MessageDummy
from tests.mock.node import NodeMock


def test_should_let_node_of_the_registered_address_handle_the_message_when_handling_sending_command():
    node = NodeMock()
    messenger = create_messenger_command_processor(nodes={
        Address("#manager0"): NodeMock(),
        Address("#manager1"): node,
        Address("#manager2"): NodeMock(),
    })
    messenger.handle_command(RegisterAddressCommand(
        address=Address("$.you"),
        node_address=Address("#manager1"),
        requester_address=Address("$"),
        ref_id="...",
    ))

    messenger.handle_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert node.handle_message__sender == Address("$.me") and \
           node.handle_message__receiver == Address("$.you") and \
           node.handle_message__message == MessageDummy("Hello")


def test_should_send_message_with_node_address_to_node_directly():
    node = NodeMock()
    messenger = create_messenger_command_processor(nodes={
        Address("#manager0"): NodeMock(),
        Address("#manager1"): node,
        Address("#manager2"): NodeMock(),
    })

    messenger.handle_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("#manager1"),
        message=MessageDummy("Hello Node"),
    ))

    assert node.handle_message__sender == Address("$.me") and \
           node.handle_message__receiver == Address("#manager1") and \
           node.handle_message__message == MessageDummy("Hello Node")


def test_should_not_raise_error_when_sending_to_unknown_node_address():
    messenger = create_messenger_command_processor()

    messenger.handle_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("#node999"),
        message=MessageDummy("Hi"),
    ))


def test_should_not_raise_error_when_sending_to_unknown_address():
    messenger = create_messenger_command_processor()

    messenger.handle_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hi"),
    ))
