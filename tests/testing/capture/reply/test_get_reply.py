from lyrid import Address
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_return_reply_with_ref_id():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.reply(Address("$"), MessageDummy("The answer is A."), ref_id="Ref123")

    assert tester.capture.get_reply("Ref123") == MessageDummy("The answer is A.")


def test_should_return_none_if_the_reply_is_not_available():
    assert ActorTester(ActorMock()).capture.get_reply("Ref123") is None


def test_should_return_reply_with_matched_ref_id():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.reply(Address("$"), MessageDummy("This is A"), ref_id="A")
    actor.reply(Address("$"), MessageDummy("This is B"), ref_id="B")

    assert tester.capture.get_reply("B") == MessageDummy("This is B")


def test_should_ignore_reply_with_other_address_than_root():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.reply(Address("$.someone"), MessageDummy("Ignore this"), ref_id="Ref123")
    actor.reply(Address("$"), MessageDummy("The is the answer"), ref_id="Ref123")

    assert tester.capture.get_reply("Ref123") == MessageDummy("The is the answer")
