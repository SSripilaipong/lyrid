from lyrid.core.manager import ActorMessageDeliveryTask
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.test_scheduler.actor_mock import WillStop


def test_should_not_pass_message_to_actor_after_actor_stopped_signal_is_raised():
    scheduler = create_scheduler()
    scheduler.start()

    actor = create_actor(WillStop)
    scheduler.register_actor(Address("$.you"), actor)

    scheduler.schedule(ActorMessageDeliveryTask(Address("$.you"), MessageDummy("Hello1"), Address("$.sender1")))
    # the actor already raised ActorStoppedSignal
    scheduler.schedule(ActorMessageDeliveryTask(Address("$.you"), MessageDummy("Hello2"), Address("$.sender2")))

    scheduler.stop()

    assert actor.receive__senders == [Address("$.sender1")] and \
           actor.receive__messages == [MessageDummy("Hello1")]
