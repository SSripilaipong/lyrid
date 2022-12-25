from lyrid import ActorProcess
from lyrid.core.messaging import Address
from lyrid.core.system import SpawnChildMessage
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.mock.messenger import MessengerMock


def test_should_send_actor_spawn_child_actor_message_to_system():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.supervisor.me"), messenger=messenger)

    child = ActorProcess(ActorMock())
    actor.spawn("my_child", child)

    assert messenger.send__sender == Address("$.supervisor.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="my_child", process=child)


def test_should_send_actor_spawn_child_actor_message_with_initial_message():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.me"), messenger=messenger)

    child = ActorProcess(ActorMock())
    actor.spawn("my_child", child, initial_message=MessageDummy("Wake Up!"))

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="my_child", initial_message=MessageDummy("Wake Up!"),
                                                        process=child)
