from lyrid.core.manager import ActorMessageDeliveryTask
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.test_scheduler.actor_mock import MyActor


def test_should_let_actor_do_scheduled_task():
    scheduler = create_scheduler()
    scheduler.start()

    actor = create_actor(MyActor)
    scheduler.register_actor(Address("$.you"), actor)

    scheduler.schedule(ActorMessageDeliveryTask(Address("$.you"), MessageDummy("Hello"), Address("$.me")))

    scheduler.stop()

    assert actor.receive__sender == Address("$.me") and \
           actor.receive__message == MessageDummy("Hello")
