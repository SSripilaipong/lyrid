from lyrid import Address
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_let_the_new_actor_receive_message_instead():
    actor1, actor2 = ActorMock(name="1"), ActorMock(name="2")
    process = create_actor_process(actor1)

    process.receive(Address("$.1"), MessageDummy("first"))
    assert actor1.on_receive__senders == [Address("$.1")] and actor1.on_receive__messages == [MessageDummy("first")]
    actor1.on_receive__clear_captures()

    actor1.become(actor2)

    process.receive(Address("$.2"), MessageDummy("second"))
    assert actor1.on_receive__senders == [] and actor1.on_receive__messages == []
    assert actor2.on_receive__senders == [Address("$.2")] and actor2.on_receive__messages == [MessageDummy("second")]
