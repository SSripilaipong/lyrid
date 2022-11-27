from lyrid.core.actor import ChildActorTerminatedMessage
from lyrid.core.manager import ActorMessageDeliveryTask
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock
from tests.scheduler.actor_mock import WillStop


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


def test_should_not_send_child_actor_terminated_message_to_the_supervisor_of_actor():
    messenger = MessengerMock()
    scheduler = create_scheduler(messenger=messenger)
    scheduler.start()

    actor = create_actor(WillStop)
    scheduler.register_actor(Address("$.supervisor.child"), actor)

    scheduler.schedule(ActorMessageDeliveryTask(
        target=Address("$.supervisor.child"),
        message=MessageDummy("Stop!"),
        sender=Address("$.someone"),
    ))

    scheduler.stop()

    assert messenger.send__message != ChildActorTerminatedMessage(child_address=Address("$.supervisor.child")) and \
           messenger.send__receiver != Address("$.supervisor")
