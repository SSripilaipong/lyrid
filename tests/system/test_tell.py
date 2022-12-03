from lyrid.core.messaging import Address
from tests.factory.system import create_actor_system
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_message_via_messenger():
    messenger = MessengerMock()
    system = create_actor_system(root_address=Address("$"), messenger=messenger)

    system.tell(Address("$.you"), MessageDummy("Hello!"))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("$.you") and \
           messenger.send__message == MessageDummy("Hello!")
