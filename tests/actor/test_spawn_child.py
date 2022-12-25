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

    child = ActorMock()
    actor.spawn("my_child", child)

    assert messenger.send__sender == Address("$.supervisor.me") and \
           messenger.send__receiver == Address("$") and \
           isinstance(messenger.send__message, SpawnChildMessage) and \
           messenger.send__message.key == "my_child" and \
           isinstance(messenger.send__message.process, ActorProcess) and \
           messenger.send__message.process.actor == child


def test_should_send_actor_spawn_child_actor_message_with_initial_message():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.me"), messenger=messenger)

    child = ActorMock()
    actor.spawn("my_child", child, initial_message=MessageDummy("Wake Up!"))

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$") and \
           isinstance(messenger.send__message, SpawnChildMessage) and \
           messenger.send__message.initial_message == MessageDummy("Wake Up!") and \
           messenger.send__message.key == "my_child" and \
           isinstance(messenger.send__message.process, ActorProcess) and \
           messenger.send__message.process.actor == child
