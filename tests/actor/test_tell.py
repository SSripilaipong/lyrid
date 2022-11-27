from lyrid.core.messaging import Address
from tests.actor.actor_mock import MyActor
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_message_via_messenger():
    messenger = MessengerMock()
    actor = create_actor(MyActor, address=Address("$.me"), messenger=messenger)

    actor.tell(Address("$.you"), MessageDummy("Hello!"))

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$.you") and \
           messenger.send__message == MessageDummy("Hello!")
