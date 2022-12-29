from lyrid import Address
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_let_actor_receive_the_message():
    actor = ActorMock()
    tester = ActorTester(actor)
    tester.simulate.tell(MessageDummy("Test Test 123"), by=Address("$.tester.me"))

    assert actor.on_receive__messages == [MessageDummy("Test Test 123")] and \
           actor.on_receive__senders == [Address("$.tester.me")]
