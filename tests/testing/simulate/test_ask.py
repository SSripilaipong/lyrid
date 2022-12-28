from lyrid import Address, Ask
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_let_actor_receive_the_message():
    actor = ActorMock()
    tester = ActorTester(actor)
    ref_id = tester.simulate.ask(MessageDummy("Test Test 123"))

    assert actor.on_receive__messages == [Ask(MessageDummy("Test Test 123"), ref_id=ref_id)] and \
           actor.on_receive__senders == [Address("$")]
