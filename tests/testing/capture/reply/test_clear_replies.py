from lyrid import Address
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_clear_all_replies():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.reply(Address("$"), MessageDummy("This is A"), ref_id="A")
    actor.reply(Address("$"), MessageDummy("This is B"), ref_id="B")
    tester.capture.clear_replies()

    assert tester.capture.get_reply("A") is None and tester.capture.get_reply("B") is None
