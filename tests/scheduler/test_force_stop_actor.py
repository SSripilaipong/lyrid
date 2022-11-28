from lyrid.core.manager import ActorMessageDeliveryTask
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.actor_mock import MyActor


def test_should_not_pass_message_to_actor_after_actor_is_forced_stopping():
    scheduler = create_scheduler()
    scheduler.start()

    actor = create_actor(MyActor)
    scheduler.register_actor(Address("$.you"), actor)

    scheduler.force_stop_actor(Address("$.you"))
    scheduler.schedule(ActorMessageDeliveryTask(Address("$.you"), MessageDummy("Hello2"), Address("$.sender2")))

    scheduler.stop()

    assert actor.receive__sender is None and actor.receive__message is None
