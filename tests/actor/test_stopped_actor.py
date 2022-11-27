import pytest

from lyrid.core.actor import ActorStoppedSignal, ChildActorStopped, SupervisorForceStop
from lyrid.core.messaging import Address
from tests.actor.actor_mock import WillStop, ChildActor, StopDummy
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_child_actor_stopped_message_to_supervisor():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.my_supervisor.me"), messenger=messenger)

    with pytest.raises(ActorStoppedSignal):
        actor.receive(Address("$.someone"), StopDummy())

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildActorStopped(child_address=Address("$.my_supervisor.me"))


def test_should_send_supervisor_force_stop_message_to_managers_of_spawned_children():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.me"), messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.receive(Address("$.someone"), StopDummy())

    assert set(messenger.send_to_manager__senders) == {Address("$.me")} and \
           set(messenger.send_to_manager__ofs) == {Address("$.me.child1"), Address("$.me.child2")} and \
           set(messenger.send_to_manager__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                                        SupervisorForceStop(address=Address("$.me.child2"))}


def test_should_send_supervisor_force_stop_message_to_not_stopped_children_only():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.me"), messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.spawn("child3", ChildActor)
    actor.receive(Address("$.me.child2"), ChildActorStopped(child_address=Address("$.me.child2")))
    actor.receive(Address("$.someone"), StopDummy())

    assert set(messenger.send_to_manager__senders) == {Address("$.me")} and \
           set(messenger.send_to_manager__ofs) == {Address("$.me.child1"), Address("$.me.child3")} and \
           set(messenger.send_to_manager__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                                        SupervisorForceStop(address=Address("$.me.child3"))}


def test_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped():
    actor = create_actor(WillStop, address=Address("$.me"))

    # noinspection DuplicatedCode
    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.spawn("child3", ChildActor)
    actor.receive(Address("$.me.child2"), ChildActorStopped(child_address=Address("$.me.child2")))
    actor.receive(Address("$.someone"), StopDummy())
    actor.receive(Address("$.me.child3"), ChildActorStopped(child_address=Address("$.me.child3")))
    actor.receive(Address("#manager6"), ChildActorStopped(child_address=Address("$.me.child3")))

    with pytest.raises(ActorStoppedSignal):
        actor.receive(Address("#manager7"), ChildActorStopped(child_address=Address("$.me.child1")))


def test_should_not_let_actor_receive_any_message_when_stopping():
    actor = create_actor(WillStop, address=Address("$.me"))

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.receive(Address("$.someone"), StopDummy())
    actor.on_receive__clear_captures()

    actor.receive(Address("$.me.child2"), ChildActorStopped(child_address=Address("$.me.child2")))
    actor.receive(Address("$.someone.else"), MessageDummy("You there?"))

    assert actor.on_receive__senders == [] and actor.on_receive__messages == []
