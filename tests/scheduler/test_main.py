from lyrid.core.messaging import Address
from lyrid.core.node import ProcessMessageDeliveryTask
from tests.factory.actor import create_actor
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.actor_mock import MyActor


def test_should_let_actor_do_scheduled_task():
    scheduler = create_scheduler()
    scheduler.start()

    actor = create_actor(MyActor)
    scheduler.register_process(Address("$.you"), actor)

    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.you"), MessageDummy("Hello"), Address("$.me")))

    scheduler.stop()

    assert actor.receive__sender == Address("$.me") and \
           actor.receive__message == MessageDummy("Hello")


def test_should_ignore_when_schedule_message_to_unknown_actor():
    scheduler = create_scheduler()
    scheduler.start()

    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.who"), MessageDummy("Hello Stranger"), Address("$.me")))

    scheduler.stop()
