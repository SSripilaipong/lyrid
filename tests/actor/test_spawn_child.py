from lyrid.core.messaging import Address
from lyrid.core.system import SpawnChildMessage
from tests.actor.actor_mock import MyActor, ChildActor
from tests.factory.actor import create_actor
from tests.mock.messenger import MessengerMock


def test_should_send_actor_spawn_child_actor_message_to_system():
    messenger = MessengerMock()
    actor = create_actor(MyActor, address=Address("$.supervisor.me"), messenger=messenger)

    actor.spawn("my_child", ChildActor)

    assert messenger.send__sender == Address("$.supervisor.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == SpawnChildMessage(key="my_child", type_=ChildActor)
