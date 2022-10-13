from lyrid import ActorBase
from lyrid.core.messaging import Address, Message
from tests.factory.actor import create_actor_with_address_and_messenger
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_message_via_messenger():
    messenger = MessengerMock()

    class MyActor(ActorBase):

        def receive(self, sender: Address, message: Message):
            self.tell(Address("$.you"), MessageDummy("Hello!"))

    actor = create_actor_with_address_and_messenger(MyActor, Address("$.me"), messenger)
    actor.receive(Address("$"), Message())

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$.you") and \
           messenger.send__message == MessageDummy("Hello!")
