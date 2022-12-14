import queue

import pytest

from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressCompletedMessage
from lyrid.core.node import NodeSpawnProcessMessage, MessageHandlingCommand, NodeSpawnProcessCompletedMessage
from lyrid.core.system import SpawnChildMessage, SpawnChildCompleted
from tests.factory.system import create_actor_system
from tests.message_dummy import MessageDummy
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.randomizer import RandomizerMock
from tests.system.process_dummy import ProcessDummy
from tests.system.util import root_process_message


def test_should_let_processor_process_handle_spawn_child_actor_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    process = ProcessDummy()
    system.handle_message(
        sender=Address("$.process"),
        receiver=Address("$"),
        message=SpawnChildMessage(key="my_child", process=process)
    )

    assert processor.process__command == MessageHandlingCommand(
        sender=Address("$.process"), receiver=Address("$"),
        message=SpawnChildMessage(key="my_child", process=process),
    )


def test_should_send_manager_spawn_actor_message_to_manager_with_generated_ref_id():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId123")
    system = create_actor_system(messenger=messenger,
                                 node_addresses=[Address("#manager1")],
                                 id_generator=id_gen)

    process = ProcessDummy()
    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", process=process))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1") and \
           messenger.send__message == \
           NodeSpawnProcessMessage(address=Address("$.process.my_child"), ref_id="GenId123", process=process)


def test_should_send_node_spawn_actor_message_with_initial_message_if_not_none():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId456")
    system = create_actor_system(messenger=messenger,
                                 node_addresses=[Address("#node0")],
                                 id_generator=id_gen)

    process = ProcessDummy()
    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", initial_message=MessageDummy("Hi!"),
                                                   process=process))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#node0") and \
           messenger.send__message == \
           NodeSpawnProcessMessage(address=Address("$.process.my_child"), initial_message=MessageDummy("Hi!"),
                                   ref_id="GenId456", process=process)


# noinspection DuplicatedCode
def test_should_send_node_spawn_process_message_to_randomly_selected_node():
    messenger = MessengerMock()
    randomizer = RandomizerMock(randrange__return=1)
    system = create_actor_system(messenger=messenger, randomizer=randomizer,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", process=ProcessDummy()))

    assert messenger.send__receiver == Address("#node1") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)


def test_should_random_range_with_number_of_node_addresses():
    id_gen = IdGeneratorMock(generate__return="GenId123")
    randomizer = RandomizerMock(randrange__return=1)
    system = create_actor_system(id_generator=id_gen, randomizer=randomizer,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", process=ProcessDummy()))

    assert randomizer.randrange__n == 3


def test_should_send_spawn_child_completed_message_to_actor_when_handling_acknowledge_messenger_register_address_completed_command():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="RefId999")
    system = create_actor_system(messenger=messenger,
                                 node_addresses=[Address("#manager1")],
                                 id_generator=id_gen)

    root_process_message(
        system, sender=Address("$.my_actor"),
        message=SpawnChildMessage(key="my_child", process=ProcessDummy()),
    )
    root_process_message(
        system, sender=Address("manager1"), message=NodeSpawnProcessCompletedMessage(
            process_address=Address("$.my_actor.my_child"), node_address=Address("#manager1"), ref_id="RefId999",
        ),
    )
    root_process_message(
        system, sender=Address("#messenger"), message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.my_actor.my_child"), manager_address=Address("#manager1"), ref_id="RefId999",
        ),
    )

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("$.my_actor") and \
           messenger.send__message == \
           SpawnChildCompleted(key="my_child", address=Address("$.my_actor.my_child"))


def test_should_not_put_reply_in_reply_queue_when_completing_spawning_child_for_actor():
    messenger = MessengerMock()
    reply_queue = queue.Queue()
    id_gen = IdGeneratorMock(generate__return="RefId999")
    system = create_actor_system(messenger=messenger, node_addresses=[Address("#manager1")],
                                 id_generator=id_gen, reply_queue=reply_queue)

    root_process_message(
        system, sender=Address("$.my_actor"),
        message=SpawnChildMessage(key="my_child", process=ProcessDummy()),
    )
    root_process_message(
        system, sender=Address("#manager1"), message=NodeSpawnProcessCompletedMessage(
            process_address=Address("$.my_actor.my_child"), node_address=Address("#manager1"), ref_id="RefId999"
        ),
    )
    root_process_message(
        system, sender=Address("#messenger"), message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.my_actor.my_child"), manager_address=Address("#manager1"), ref_id="RefId999",
        ),
    )

    with pytest.raises(queue.Empty):
        reply_queue.get(block=False)
