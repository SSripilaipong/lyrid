from lyrid import ActorBase
from lyrid.core.messaging import Address, Message
from lyrid.core.system import ActorSpawnChildActorMessage
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_actor_spawn_child_actor_message_to_system():
    messenger = MessengerMock()

    class MyActor(ActorBase):

        def receive(self, sender: Address, message: Message):
            self.spawn("my_child", ChildActor)

    actor = create_actor(MyActor, address=Address("$.supervisor.me"), messenger=messenger)
    actor.receive(Address("$"), MessageDummy(""))

    assert messenger.send__sender == Address("$.supervisor.me") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == ActorSpawnChildActorMessage(key="my_child", type_=ChildActor)


class ChildActor(ActorBase):

    def receive(self, sender: Address, message: Message):
        pass
