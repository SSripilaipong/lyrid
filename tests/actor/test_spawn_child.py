from lyrid import ActorProcess
from lyrid.core.messaging import Address
from lyrid.core.system import SpawnChildMessage
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock


def test_should_send_actor_spawn_child_actor_message_to_system():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.supervisor.me"), messenger=messenger)

    child = ActorMock()
    actor.spawn(child, key="my_child")

    assert messenger.send__sender == Address("$.supervisor.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="my_child", process=ActorProcess(child))


def test_should_generate_random_key_when_not_specified():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.parent"), messenger=messenger,
                             id_gen=IdGeneratorMock(generate__return="Id999"))

    child = ActorMock()
    actor.spawn(child)

    assert messenger.send__sender == Address("$.parent") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="Id999", process=ActorProcess(child))


def test_should_send_actor_spawn_child_actor_message_with_initial_message():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.me"), messenger=messenger)

    child = ActorMock()
    actor.spawn(child, key="my_child", initial_message=MessageDummy("Wake Up!"))

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="my_child", process=ActorProcess(child),
                                                        initial_message=MessageDummy("Wake Up!"))


def test_should_return_address():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.me"), messenger=messenger)

    assert actor.spawn(ActorMock(), key="you") == Address("$.me.you")


def test_should_return_address_with_random_key_if_used():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.parent.me"), messenger=messenger,
                             id_gen=IdGeneratorMock(generate__return="Id999"))

    assert actor.spawn(ActorMock()) == Address("$.parent.me.Id999")
