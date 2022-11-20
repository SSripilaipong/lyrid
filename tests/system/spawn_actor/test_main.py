from lyrid.core.manager import ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressMessage, MessengerRegisterAddressCompletedMessage
from lyrid.core.system import AcknowledgeManagerSpawnActorCompletedCommand, \
    AcknowledgeMessengerRegisterAddressCompletedCommand
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock


def test_should_let_processor_process_acknowledge_spawn_actor_completed_command_when_handling_message_manager_spawn_actor_completed_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.handle_message(
        sender=Address("#manager1"),
        receiver=Address("$"),
        message=ManagerSpawnActorCompletedMessage(actor_address=Address("$.new"), manager_address=Address("#manager1"))
    )

    assert processor.process__command == AcknowledgeManagerSpawnActorCompletedCommand(
        actor_address=Address("$.new"), manager_address=Address("#manager1"),
    )


def test_should_send_messenger_register_address_message_to_messenger_when_handling_acknowledge_manager_spawn_actor_completed_command():
    messenger = MessengerMock()
    system = create_actor_system(address=Address("$"), messenger=messenger, messenger_address=Address("#messenger"))

    system.handle_processor_command(AcknowledgeManagerSpawnActorCompletedCommand(
        actor_address=Address("$.new"), manager_address=Address("#manager1"),
    ))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#messenger") and \
           messenger.send__message == MessengerRegisterAddressMessage(address=Address("$.new"),
                                                                      manager_address=Address("#manager1"))


def test_should_let_processor_process_acknowledge_messenger_register_address_completed_command_when_handling_messenger_register_address_completed_message():
    processor = ProcessorMock()
    system = create_actor_system(messenger_address=Address("#messenger"), processor=processor)

    system.handle_message(
        sender=Address("#messenger"),
        receiver=Address("$"),
        message=MessengerRegisterAddressCompletedMessage(address=Address("$.new"), manager_address=Address("#manager1"))
    )

    assert processor.process__command == AcknowledgeMessengerRegisterAddressCompletedCommand(
        actor_address=Address("$.new"), manager_address=Address("#manager1"),
    )
