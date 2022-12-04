from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingCommand, RegisterAddressCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.mock.node import NodeMock
from tests.mock.processor import ProcessorMock


def test_should_pass_sending_command_to_processor_when_send_method_is_called():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send(Address("$.me"), Address("$.you"), MessageDummy("Hello"))

    assert processor.process__command == SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    )


def test_should_let_manager_of_the_registered_address_handle_the_message_when_handling_sending_command():
    manager = NodeMock()
    messenger = create_messenger(nodes={
        Address("#manager0"): NodeMock(),
        Address("#manager1"): manager,
        Address("#manager2"): NodeMock(),
    })
    messenger.handle_processor_command(RegisterAddressCommand(
        address=Address("$.you"),
        node_address=Address("#manager1"),
        requester_address=Address("$"),
        ref_id="...",
    ))

    messenger.handle_processor_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert manager.handle_message__sender == Address("$.me") and \
           manager.handle_message__receiver == Address("$.you") and \
           manager.handle_message__message == MessageDummy("Hello")


def test_should_send_message_with_manager_address_to_manager_directly():
    manager = NodeMock()
    messenger = create_messenger(nodes={
        Address("#manager0"): NodeMock(),
        Address("#manager1"): manager,
        Address("#manager2"): NodeMock(),
    })

    messenger.handle_processor_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("#manager1"),
        message=MessageDummy("Hello Manager"),
    ))

    assert manager.handle_message__sender == Address("$.me") and \
           manager.handle_message__receiver == Address("#manager1") and \
           manager.handle_message__message == MessageDummy("Hello Manager")


def test_should_not_raise_error_when_sending_to_unknown_node_address():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.handle_processor_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("#node999"),
        message=MessageDummy("Hi"),
    ))


def test_should_not_raise_error_when_sending_to_unknown_address():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.handle_processor_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hi"),
    ))
