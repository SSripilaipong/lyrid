from lyrid import ChildStopped
from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_let_actor_receive_child_stopped_message_with_key():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.child_stop(key="ChildKey123")

    assert actor.on_receive__messages == [
        ChildStopped(tester.actor_address.child("ChildKey123"), exception=None),
    ] and actor.on_receive__senders == [tester.actor_address]
