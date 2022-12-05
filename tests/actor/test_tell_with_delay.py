from lyrid.core.messaging import Address
from tests.actor.actor_mock import MyActor
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_not_send_message_via_messenger_immediately():
    messenger = MessengerMock()

    actor = create_actor(MyActor, address=Address("$.me"), messenger=messenger)

    actor.tell(Address("$.you"), MessageDummy("Hello!"), delay=555.123)

    assert messenger.send__sender is None and messenger.send__receiver is None and messenger.send__message is None
