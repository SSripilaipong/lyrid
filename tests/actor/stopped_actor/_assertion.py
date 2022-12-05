from typing import Callable, Type, List

# noinspection PyPackageRequirements
import pytest

from lyrid import VanillaActor
from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessStoppedSignal, ChildStopped, SupervisorForceStop
from tests.actor.actor_mock import ChildActor
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def assert_should_send_child_actor_stopped_message_to_supervisor(actor_type: Type[VanillaActor],
                                                                 stop: Callable[[VanillaActor, Address], None]):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    actor = create_actor(actor_type, address=my_address, messenger=messenger)

    with pytest.raises(ProcessStoppedSignal):
        stop(actor, my_address)

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildStopped(child_address=Address("$.my_supervisor.me"))


def assert_should_send_supervisor_force_stop_message_to_spawned_children(actor_type: Type[VanillaActor],
                                                                         stop: Callable[[VanillaActor, Address], None]):
    my_address = Address("$.me")
    messenger = MessengerMock()
    actor = create_actor(actor_type, address=my_address, messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    messenger.send__clear_captures()
    stop(actor, my_address)

    print(messenger.send__messages)
    assert set(messenger.send__senders) == {Address("$.me")} and \
           set(messenger.send__receivers) == {Address("$.me.child1"), Address("$.me.child2")} and \
           set(messenger.send__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                             SupervisorForceStop(address=Address("$.me.child2"))}


def assert_should_send_supervisor_force_stop_message_to_not_stopped_children_only(actor_type: Type[VanillaActor],
                                                                                  stop: Callable[
                                                                                      [VanillaActor, Address], None]):
    my_address = Address("$.me")
    messenger = MessengerMock()
    actor = create_actor(actor_type, address=my_address, messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.spawn("child3", ChildActor)
    actor.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    messenger.send__clear_captures()
    stop(actor, my_address)

    assert set(messenger.send__senders) == {Address("$.me")} and \
           set(messenger.send__receivers) == {Address("$.me.child1"), Address("$.me.child3")} and \
           set(messenger.send__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                             SupervisorForceStop(address=Address("$.me.child3"))}


def assert_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped(
        actor_type: Type[VanillaActor],
        stop: Callable[[VanillaActor, Address], None]):
    my_address = Address("$.me")
    actor = create_actor(actor_type, address=my_address)

    # noinspection DuplicatedCode
    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    actor.spawn("child3", ChildActor)
    actor.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    stop(actor, my_address)
    actor.receive(Address("$.me.child3"), ChildStopped(child_address=Address("$.me.child3")))
    actor.receive(Address("#manager6"), ChildStopped(child_address=Address("$.me.child3")))

    with pytest.raises(ProcessStoppedSignal):
        actor.receive(Address("#manager7"), ChildStopped(child_address=Address("$.me.child1")))


def assert_should_not_let_actor_receive_any_message_when_stopping(
        actor_type: Type[VanillaActor],
        stop: Callable[[VanillaActor, Address], None],
        on_receive__clear_captures: Callable[[VanillaActor], None],
        on_receive__senders: Callable[[VanillaActor], List[Address]],
        on_receive__messages: Callable[[VanillaActor], List[Message]],
):
    my_address = Address("$.me")
    actor = create_actor(actor_type, address=my_address)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    stop(actor, my_address)
    on_receive__clear_captures(actor)

    actor.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    actor.receive(Address("$.someone.else"), MessageDummy("You there?"))

    assert on_receive__senders(actor) == [] and on_receive__messages(actor) == []


def assert_should_call_on_stop_after_actor_raising_process_stop_signal(actor_type: Type[VanillaActor],
                                                                       stop: Callable[[VanillaActor, Address], None],
                                                                       on_stop__is_called: Callable[
                                                                           [VanillaActor], bool]):
    my_address = Address("$.me")
    actor = create_actor(actor_type, address=my_address)

    with pytest.raises(ProcessStoppedSignal):
        stop(actor, my_address)

    assert on_stop__is_called(actor)


def assert_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped(
        actor_type: Type[VanillaActor],
        stop: Callable[[VanillaActor, Address], None],
):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    actor = create_actor(actor_type, address=my_address, messenger=messenger)

    actor.spawn("child2", ChildActor)
    stop(actor, my_address)
    messenger.send__clear_captures()

    with pytest.raises(ProcessStoppedSignal):
        actor.receive(Address("$.my_supervisor.me.child2"),
                      ChildStopped(child_address=Address("$.my_supervisor.me.child2")))

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildStopped(child_address=Address("$.my_supervisor.me"))


def assert_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped(
        actor_type: Type[VanillaActor],
        stop: Callable[[VanillaActor, Address], None],
):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    actor = create_actor(actor_type, address=my_address, messenger=messenger)

    actor.spawn("child1", ChildActor)
    actor.spawn("child2", ChildActor)
    stop(actor, my_address)
    actor.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))

    assert not any(isinstance(m, ChildStopped) for m in messenger.send__messages)


def assert_should_ignore_any_exception_when_running_on_stop(
        actor_type: Type[VanillaActor],
        stop: Callable[[VanillaActor, Address], None],
):
    my_address = Address("$.my_supervisor.me")
    actor = create_actor(actor_type, address=my_address)

    def on_stop():
        raise Exception()

    actor.on_stop = on_stop  # type: ignore

    with pytest.raises(ProcessStoppedSignal):
        stop(actor, my_address)
