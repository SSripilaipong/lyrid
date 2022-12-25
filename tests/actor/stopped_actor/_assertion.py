from typing import Callable, List

# noinspection PyPackageRequirements
import pytest

from lyrid import Actor, ActorProcess
from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessStoppedSignal, ChildStopped, SupervisorForceStop
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.mock.messenger import MessengerMock


def assert_should_send_child_actor_stopped_message_to_supervisor(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
        exception: Exception = None,
):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    process = create_actor_process(actor_factory(), address=my_address, messenger=messenger)

    with pytest.raises(ProcessStoppedSignal):
        stop(process, my_address)

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildStopped(child_address=Address("$.my_supervisor.me"), exception=exception)


# noinspection DuplicatedCode
def assert_should_send_supervisor_force_stop_message_to_spawned_children(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
):
    my_address = Address("$.me")
    messenger = MessengerMock()
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address, messenger=messenger)

    actor.spawn(ActorMock(), key="child1")
    actor.spawn(ActorMock(), key="child2")
    messenger.send__clear_captures()
    stop(process, my_address)

    assert set(messenger.send__senders) == {Address("$.me")} and \
           set(messenger.send__receivers) == {Address("$.me.child1"), Address("$.me.child2")} and \
           set(messenger.send__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                             SupervisorForceStop(address=Address("$.me.child2"))}


# noinspection DuplicatedCode
def assert_should_send_supervisor_force_stop_message_to_not_stopped_children_only(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
):
    my_address = Address("$.me")
    messenger = MessengerMock()
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address, messenger=messenger)

    actor.spawn(ActorMock(), key="child1")
    actor.spawn(ActorMock(), key="child2")
    actor.spawn(ActorMock(), key="child3")
    process.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    messenger.send__clear_captures()
    stop(process, my_address)

    assert set(messenger.send__senders) == {Address("$.me")} and \
           set(messenger.send__receivers) == {Address("$.me.child1"), Address("$.me.child3")} and \
           set(messenger.send__messages) == {SupervisorForceStop(address=Address("$.me.child1")),
                                             SupervisorForceStop(address=Address("$.me.child3"))}


def assert_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
):
    my_address = Address("$.me")
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address)

    # noinspection DuplicatedCode
    actor.spawn(ActorMock(), key="child1")
    actor.spawn(ActorMock(), key="child2")
    actor.spawn(ActorMock(), key="child3")
    process.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    stop(process, my_address)
    process.receive(Address("$.me.child3"), ChildStopped(child_address=Address("$.me.child3")))
    process.receive(Address("#manager6"), ChildStopped(child_address=Address("$.me.child3")))

    with pytest.raises(ProcessStoppedSignal):
        process.receive(Address("#manager7"), ChildStopped(child_address=Address("$.me.child1")))


def assert_should_not_let_actor_receive_any_message_when_stopping(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
        on_receive__clear_captures: Callable[[Actor], None],
        on_receive__senders: Callable[[Actor], List[Address]],
        on_receive__messages: Callable[[Actor], List[Message]],
):
    my_address = Address("$.me")
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address)

    actor.spawn(ActorMock(), key="child1")
    actor.spawn(ActorMock(), key="child2")
    stop(process, my_address)
    on_receive__clear_captures(actor)

    process.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))
    process.receive(Address("$.someone.else"), MessageDummy("You there?"))

    assert on_receive__senders(actor) == [] and on_receive__messages(actor) == []


def assert_should_call_on_stop_after_actor_raising_process_stop_signal(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
        on_stop__is_called: Callable[[Actor], bool],
):
    my_address = Address("$.me")
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address)

    with pytest.raises(ProcessStoppedSignal):
        stop(process, my_address)

    assert on_stop__is_called(actor)


def assert_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
        exception: Exception = None,
):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address, messenger=messenger)

    actor.spawn(ActorMock(), key="child2")
    stop(process, my_address)
    messenger.send__clear_captures()

    with pytest.raises(ProcessStoppedSignal):
        process.receive(Address("$.my_supervisor.me.child2"),
                        ChildStopped(child_address=Address("$.my_supervisor.me.child2")))

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildStopped(child_address=Address("$.my_supervisor.me"), exception=exception)


def assert_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
):
    my_address = Address("$.my_supervisor.me")
    messenger = MessengerMock()
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address, messenger=messenger)

    actor.spawn(ActorMock(), key="child1")
    actor.spawn(ActorMock(), key="child2")
    stop(process, my_address)
    process.receive(Address("$.me.child2"), ChildStopped(child_address=Address("$.me.child2")))

    assert not any(isinstance(m, ChildStopped) for m in messenger.send__messages)


def assert_should_ignore_any_exception_when_running_on_stop(
        actor_factory: Callable[[], Actor],
        stop: Callable[[ActorProcess, Address], None],
):
    my_address = Address("$.my_supervisor.me")
    actor = actor_factory()
    process = create_actor_process(actor, address=my_address)

    def on_stop():
        raise Exception()

    actor.on_stop = on_stop  # type: ignore

    with pytest.raises(ProcessStoppedSignal):
        stop(process, my_address)
