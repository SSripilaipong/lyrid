import queue

from lyrid import ActorProcess
from lyrid.core.messaging import Address
from lyrid.core.messenger import MessengerRegisterAddressCompletedMessage
from lyrid.core.node import NodeSpawnProcessMessage
from lyrid.core.system import SystemSpawnActorCommand, SystemSpawnActorCompletedReply
from tests.factory.system import create_actor_system
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.randomizer import RandomizerMock
from tests.system.process_dummy import ProcessDummy
from tests.system.util import root_process_message


def test_should_let_processor_process_spawn_actor_command_when_spawn_is_called():
    processor = ProcessorMock()
    reply_queue = queue.Queue()
    reply_queue.put(SystemSpawnActorCompletedReply(address=Address("$.hello")))
    system = create_actor_system(processor=processor, reply_queue=reply_queue)

    actor = ActorMock()
    system.spawn("hello", actor)

    assert isinstance(processor.process__command, SystemSpawnActorCommand) and \
           processor.process__command.key == "hello" and \
           isinstance(processor.process__command.process, ActorProcess) and \
           processor.process__command.process.actor == actor


def test_should_let_processor_process_spawn_actor_command_with_initial_message_if_not_none():
    processor = ProcessorMock()
    reply_queue = queue.Queue()
    reply_queue.put(SystemSpawnActorCompletedReply(address=Address("$.hello")))
    system = create_actor_system(processor=processor, reply_queue=reply_queue)

    actor = ActorMock()
    system.spawn("hello", actor, initial_message=MessageDummy("Do It!"))

    assert isinstance(processor.process__command, SystemSpawnActorCommand) and \
           processor.process__command.key == "hello" and \
           processor.process__command.initial_message == MessageDummy("Do It!") and \
           isinstance(processor.process__command.process, ActorProcess) and \
           processor.process__command.process.actor == actor


def test_should_send_spawn_actor_message_to_manager_via_messenger_when_handling_spawn_actor_processor_command():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId123")
    system = create_actor_system(address=Address("$"), messenger=messenger,
                                 node_addresses=[Address("#manager1")], id_generator=id_gen)

    process = ProcessDummy()
    system.handle_processor_command(SystemSpawnActorCommand(key="hello", process=process))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1") and \
           messenger.send__message == \
           NodeSpawnProcessMessage(address=Address("$.hello"), ref_id="GenId123", process=process)


def test_should_send_node_spawn_actor_message_with_initial_message_if_not_none():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId456")
    system = create_actor_system(messenger=messenger,
                                 node_addresses=[Address("#node0")],
                                 id_generator=id_gen)

    process = ProcessDummy()
    system.handle_processor_command(
        SystemSpawnActorCommand(key="hello", process=process, initial_message=MessageDummy("Hey!")))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#node0") and \
           messenger.send__message == \
           NodeSpawnProcessMessage(address=Address("$.hello"), initial_message=MessageDummy("Hey!"), ref_id="GenId456",
                                   process=process)


def test_should_send_node_spawn_process_message_to_randomly_selected_node():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId123")
    randomizer = RandomizerMock(randrange__return=1)
    system = create_actor_system(messenger=messenger, id_generator=id_gen, randomizer=randomizer,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    system.handle_processor_command(SystemSpawnActorCommand(key="hello", process=ProcessDummy()))

    assert messenger.send__receiver == Address("#node1")


def test_should_random_range_with_number_of_node_addresses():
    id_gen = IdGeneratorMock(generate__return="GenId123")
    randomizer = RandomizerMock(randrange__return=1)
    system = create_actor_system(id_generator=id_gen, randomizer=randomizer,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    system.handle_processor_command(SystemSpawnActorCommand(key="hello", process=ProcessDummy()))

    assert randomizer.randrange__n == 3


def test_should_put_system_spawn_actor_completed_reply_to_reply_queue_when_handling_acknowledge_messenger_register_address_completed_command():
    reply_queue = queue.Queue()
    system = create_actor_system(reply_queue=reply_queue)

    root_process_message(
        system, sender=Address("#messenger"), message=MessengerRegisterAddressCompletedMessage(
            address=Address("$.new"), manager_address=Address("#manager1"), ref_id="RefId999",
        ),
    )

    assert reply_queue.get() == SystemSpawnActorCompletedReply(address=Address("$.new"))


def test_should_get_reply_from_reply_queue_and_return_spawned_address():
    reply_queue = queue.Queue()
    reply_queue.put(SystemSpawnActorCompletedReply(address=Address("$.new")))
    system = create_actor_system(reply_queue=reply_queue)

    address = system.spawn("new", ActorMock())

    assert address == Address("$.new")
