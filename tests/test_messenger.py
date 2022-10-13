from lyrid.core.messenger import Address, SendingCommand, RegisterAddressCommand
from lyrid.message import TextMessage
from tests.manager_mock import ManagerMock
from tests.messenger_factory import create_messenger
from tests.processor_mock import ProcessorMock


def test_should_pass_sending_command_to_processor_when_send_method_is_called():
    processor = ProcessorMock()
    messenger = create_messenger(processor=processor)

    messenger.send(Address("$.me"), Address("$.you"), TextMessage("Hello"))

    assert processor.process_command == SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=TextMessage("Hello"),
    )


def test_should_let_manager_of_the_registered_address_handle_the_message_when_handling_sending_command():
    manager = ManagerMock()
    messenger = create_messenger(managers={
        "manager0": ManagerMock(),
        "manager1": manager,
        "manager2": ManagerMock(),
    })
    messenger.handle_processor_command(RegisterAddressCommand(
        addr=Address("$.you"),
        manager_key="manager1",
    ))

    messenger.handle_processor_command(SendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=TextMessage("Hello"),
    ))

    assert manager.handle_sender == Address("$.me") and \
           manager.handle_receiver == Address("$.you") and \
           manager.handle_message == TextMessage("Hello")
