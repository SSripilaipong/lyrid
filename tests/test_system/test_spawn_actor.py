import queue

from lyrid.core.manager import ManagerSpawnActorMessage, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressMessage
from lyrid.core.system import SystemSpawnActorCommand, AcknowledgeManagerSpawnActorCompletedCommand, \
    AcknowledgeMessengerRegisterAddressCompletedCommand, SystemSpawnActorCompletedReply
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.test_system.actor_dummy import MyActor


def test_should_send_spawn_actor_message_to_manager_via_messenger_when_handling_spawn_actor_processor_command():
    messenger = MessengerMock()
    system = create_actor_system(address=Address("$"), messenger=messenger, manager_addresses=[Address("#manager1")])

    system.handle_processor_command(SystemSpawnActorCommand(key="hello", type_=MyActor))

    assert messenger.send__message == ManagerSpawnActorMessage(address=Address("$.hello"), type_=MyActor) and \
           messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1")


def test_should_let_processor_process_spawn_actor_command_when_spawn_is_called():
    processor = ProcessorMock()
    reply_queue = queue.Queue()
    reply_queue.put(SystemSpawnActorCompletedReply(address=Address("$.hello")))
    system = create_actor_system(processor=processor, reply_queue=reply_queue)

    system.spawn("hello", MyActor)

    assert processor.process__command == SystemSpawnActorCommand(key="hello", type_=MyActor)


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


def test_should_put_system_spawn_actor_completed_reply_to_reply_queue_when_handling_acknowledge_messenger_register_address_completed_command():
    reply_queue = queue.Queue()
    system = create_actor_system(reply_queue=reply_queue)

    system.handle_processor_command(AcknowledgeMessengerRegisterAddressCompletedCommand(
        actor_address=Address("$.new"), manager_address=Address("#manager1"),
    ))

    assert reply_queue.get() == SystemSpawnActorCompletedReply(address=Address("$.new"))


def test_should_get_reply_from_reply_queue_and_return_spawned_address():
    reply_queue = queue.Queue()
    reply_queue.put(SystemSpawnActorCompletedReply(address=Address("$.new")))
    system = create_actor_system(reply_queue=reply_queue)

    address = system.spawn("new", MyActor)

    assert address == Address("$.new")