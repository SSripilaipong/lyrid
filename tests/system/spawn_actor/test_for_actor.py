import queue

import pytest

from lyrid.core.manager import ManagerSpawnActorMessage, ActorMessageSendingCommand, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address
from lyrid.core.system import SpawnChildMessage, ActorSpawnChildActorCommand, \
    AcknowledgeMessengerRegisterAddressCompletedCommand, SpawnChildCompletedMessage
from tests.factory.system import create_actor_system
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.system.actor_dummy import ActorDummy


def test_should_let_processor_process_actor_spawn_child_actor_command_when_handling_actor_spawn_child_actor_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.handle_message(
        sender=Address("$.actor"),
        receiver=Address("$"),
        message=SpawnChildMessage(key="my_child", type_=ActorDummy)
    )

    assert processor.process__command == ActorSpawnChildActorCommand(
        actor_address=Address("$.actor"), child_key="my_child", child_type=ActorDummy,
    )


def test_should_send_manager_spawn_actor_message_to_manager_with_generated_ref_id():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId123")
    system = create_actor_system(messenger=messenger,
                                 manager_addresses=[Address("#manager1")],
                                 id_generator=id_gen)

    system.handle_processor_command(ActorSpawnChildActorCommand(
        actor_address=Address("$.actor"), child_key="my_child", child_type=ActorDummy,
    ))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1") and \
           messenger.send__message == \
           ManagerSpawnActorMessage(address=Address("$.actor.my_child"), type_=ActorDummy, ref_id="GenId123")


def test_should_send_spawn_child_completed_message_to_actor_when_handling_acknowledge_messenger_register_address_completed_command():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="RefId999")
    system = create_actor_system(messenger=messenger,
                                 manager_addresses=[Address("#manager1")],
                                 id_generator=id_gen)

    # noinspection DuplicatedCode
    system.handle_processor_command(ActorSpawnChildActorCommand(
        actor_address=Address("$.my_actor"), child_key="my_child", child_type=ActorDummy,
    ))
    system.handle_processor_command(ActorMessageSendingCommand(
        sender=Address("#manager1"), receiver=Address("$"),
        message=ManagerSpawnActorCompletedMessage(
            actor_address=Address("$.my_actor.my_child"),
            manager_address=Address("#manager1"),
            ref_id="RefId999"
        )))
    system.handle_processor_command(AcknowledgeMessengerRegisterAddressCompletedCommand(
        actor_address=Address("$.my_actor.my_child"), manager_address=Address("#manager1"), ref_id="RefId999",
    ))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("$.my_actor") and \
           messenger.send__message == \
           SpawnChildCompletedMessage(key="my_child", address=Address("$.my_actor.my_child"))


def test_should_not_put_reply_in_reply_queue_when_completing_spawning_child_for_actor():
    messenger = MessengerMock()
    reply_queue = queue.Queue()
    id_gen = IdGeneratorMock(generate__return="RefId999")
    system = create_actor_system(messenger=messenger, manager_addresses=[Address("#manager1")],
                                 id_generator=id_gen, reply_queue=reply_queue)

    # noinspection DuplicatedCode
    system.handle_processor_command(ActorSpawnChildActorCommand(
        actor_address=Address("$.my_actor"), child_key="my_child", child_type=ActorDummy,
    ))
    system.handle_processor_command(ActorMessageSendingCommand(
        sender=Address("#manager1"), receiver=Address("$"),
        message=ManagerSpawnActorCompletedMessage(
            actor_address=Address("$.my_actor.my_child"),
            manager_address=Address("#manager1"),
            ref_id="RefId999"
        )))
    system.handle_processor_command(AcknowledgeMessengerRegisterAddressCompletedCommand(
        actor_address=Address("$.my_actor.my_child"), manager_address=Address("#manager1"), ref_id="RefId999",
    ))

    with pytest.raises(queue.Empty):
        reply_queue.get(block=False)
