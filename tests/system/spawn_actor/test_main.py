from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressMessage, MessengerRegisterAddressCompletedMessage
from lyrid.core.node import NodeSpawnProcessCompletedMessage, MessageHandlingCommand
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.system.util import root_process_message


def test_should_let_processor_process_handle_manager_spawn_actor_completed_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.handle_message(
        sender=Address("#manager1"),
        receiver=Address("$"),
        message=NodeSpawnProcessCompletedMessage(actor_address=Address("$.new"), manager_address=Address("#manager1"),
                                                 ref_id="RefId123")
    )

    assert processor.process__command == MessageHandlingCommand(
        sender=Address("#manager1"), receiver=Address("$"),
        message=NodeSpawnProcessCompletedMessage(
            actor_address=Address("$.new"),
            manager_address=Address("#manager1"),
            ref_id="RefId123",
        ),
    )


def test_should_send_messenger_register_address_message_to_messenger_when_handling_manager_spawn_actor_completed_message():
    messenger = MessengerMock()
    system = create_actor_system(address=Address("$"), messenger=messenger, messenger_address=Address("#messenger"))

    root_process_message(
        system, sender=Address("#manager1"), message=NodeSpawnProcessCompletedMessage(
            actor_address=Address("$.new"), manager_address=Address("#manager1"), ref_id="RefId999",
        ),
    )

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#messenger") and \
           messenger.send__message == MessengerRegisterAddressMessage(address=Address("$.new"),
                                                                      manager_address=Address("#manager1"),
                                                                      ref_id="RefId999")


def test_should_let_processor_process_acknowledge_messenger_register_address_completed_command_when_handling_messenger_register_address_completed_message():
    processor = ProcessorMock()
    system = create_actor_system(messenger_address=Address("#messenger"), processor=processor)

    system.handle_message(
        sender=Address("#messenger"),
        receiver=Address("$"),
        message=MessengerRegisterAddressCompletedMessage(address=Address("$.new"), manager_address=Address("#manager1"),
                                                         ref_id="RefId123")
    )

    assert processor.process__command == MessageHandlingCommand(
        sender=Address("#messenger"), receiver=Address("$"),
        message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.new"), manager_address=Address("#manager1"), ref_id="RefId123",
        ),
    )
