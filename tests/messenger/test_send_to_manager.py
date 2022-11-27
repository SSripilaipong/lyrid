from lyrid.core.messaging import Address
from lyrid.core.messenger import SendingToManagerCommand, RegisterAddressCommand
from tests.factory.messenger import create_messenger
from tests.message_dummy import MessageDummy
from tests.mock.manager import ManagerMock
from tests.mock.processor import ProcessorMock


def test_should_pass_sending_to_manager_command_to_processor_when_send_to_manager_method_is_called():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send_to_manager(sender=Address("$.me"), of=Address("$.you"), message=MessageDummy("Hello"))

    assert processor.process__command == SendingToManagerCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    )


def test_should_let_manager_of_the_registered_address_handle_the_message_to_itself_when_handling_sending_to_manager_command():
    # noinspection DuplicatedCode
    manager = ManagerMock()
    messenger = create_messenger(managers={
        Address("#manager1"): ManagerMock(),
        Address("#manager2"): manager,
        Address("#manager3"): ManagerMock(),
    })
    messenger.handle_processor_command(RegisterAddressCommand(
        address=Address("$.you"),
        manager_address=Address("#manager2"),
        requester_address=Address("$"),
        ref_id="...",
    ))

    messenger.handle_processor_command(SendingToManagerCommand(
        sender=Address("$.me"),
        of=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert manager.handle_message__sender == Address("$.me") and \
           manager.handle_message__receiver == Address("#manager2") and \
           manager.handle_message__message == MessageDummy("Hello")
