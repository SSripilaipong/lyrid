from lyrid.core.messaging import Address
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_clear_messages():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.to.you"), MessageDummy("Hi now"))
    actor.tell(Address("$.other"), MessageDummy("Hi later"), delay=123)
    tester.capture.clear_messages()

    assert tester.capture.get_messages() == []
