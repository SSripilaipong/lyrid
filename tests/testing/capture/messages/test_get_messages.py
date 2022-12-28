from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock, ActorMockStop


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


def test_should_return_messages_with_or_without_delay_in_any_order():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.to.you"), MessageDummy("Hi now"))
    actor.tell(Address("$.other"), MessageDummy("Hi later"), delay=123)

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(Address("$.other"), MessageDummy("Hi later"), delay=123),
        CapturedMessage(Address("$.to.you"), MessageDummy("Hi now"), delay=None),
    }


def test_should_ignore_reply_messages():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.to.you"), MessageDummy("Hi now"))
    actor.reply(Address("$.user"), MessageDummy("Hey User!"), ref_id="RefId1234")

    assert tester.capture.get_messages() == [
        CapturedMessage(Address("$.to.you"), MessageDummy("Hi now"), delay=None),
    ]


def test_should_ignore_spawn_messages():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.you"), MessageDummy("Important"))
    actor.spawn(ActorMock())

    assert tester.capture.get_messages() == [
        CapturedMessage(Address("$.you"), MessageDummy("Important"), delay=None),
    ]


def test_should_ignore_child_stopped_messages_when_stopping():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.tell(Address("$.you"), MessageDummy("Important"))
    tester.simulate.tell(ActorMockStop(), Address("$.me"))

    assert tester.capture.get_messages() == [
        CapturedMessage(Address("$.you"), MessageDummy("Important"), delay=None),
    ]
