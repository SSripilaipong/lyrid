import pytest

from lyrid.core.actor import ActorStoppedSignal, ChildActorStopped, SupervisorForceStop
from lyrid.core.messaging import Address
from tests.actor.actor_mock import WillStop, ChildActor
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_child_actor_stopped_message_to_supervisor():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.my_supervisor.me"), messenger=messenger)

    with pytest.raises(ActorStoppedSignal):
        actor.receive(Address("$.someone"), MessageDummy("STOPP"))

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildActorStopped(child_address=Address("$.my_supervisor.me"))


def test_should_send_supervisor_force_stop_message_to_managers_of_spawned_children():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.me"), messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.receive(Address("$.someone"), MessageDummy("STOPP"))

    assert messenger.send_to_manager__senders == [Address("$.me"), Address("$.me")] and \
           messenger.send_to_manager__ofs == [Address("$.me.child1"), Address("$.me.child2")] and \
           messenger.send_to_manager__messages == [SupervisorForceStop(), SupervisorForceStop()]
