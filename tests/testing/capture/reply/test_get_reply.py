from lyrid import Address
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_return_replies_with_ref_id():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.reply(Address("$"), MessageDummy("The answer is A."), ref_id="Ref123")

    assert tester.capture.get_reply("Ref123") == MessageDummy("The answer is A.")
