from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_return_told_messages():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.to.you"), MessageDummy("Hi now"))

    assert tester.capture.get_messages() == [
        CapturedMessage(Address("$.to.you"), MessageDummy("Hi now"), delay=None),
    ]


def test_should_return_told_messages_with_delay():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.other"), MessageDummy("Hi later"), delay=123)

    assert tester.capture.get_messages() == [
        CapturedMessage(Address("$.other"), MessageDummy("Hi later"), delay=123),
    ]
