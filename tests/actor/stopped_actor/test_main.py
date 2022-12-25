from typing import List

from lyrid import ActorProcess, Actor
from lyrid.core.messaging import Address, Message
from tests.actor.stopped_actor._assertion import assert_should_send_child_actor_stopped_message_to_supervisor, \
    assert_should_send_supervisor_force_stop_message_to_spawned_children, \
    assert_should_send_supervisor_force_stop_message_to_not_stopped_children_only, \
    assert_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped, \
    assert_should_not_let_actor_receive_any_message_when_stopping, \
    assert_should_call_on_stop_after_actor_raising_process_stop_signal, \
    assert_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped, \
    assert_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped, \
    assert_should_ignore_any_exception_when_running_on_stop
from tests.mock.actor import ActorMockStop, ActorMock


def test_should_send_child_actor_stopped_message_to_supervisor():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_send_child_actor_stopped_message_to_supervisor(lambda: ActorMock(), stop)


def test_should_send_supervisor_force_stop_message_to_spawned_children():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_send_supervisor_force_stop_message_to_spawned_children(lambda: ActorMock(), stop)


def test_should_send_supervisor_force_stop_message_to_not_stopped_children_only():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_send_supervisor_force_stop_message_to_not_stopped_children_only(lambda: ActorMock(), stop)


def test_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped(
        lambda: ActorMock(), stop,
    )


def test_should_not_let_actor_receive_any_message_when_stopping():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    # noinspection DuplicatedCode
    def on_receive__clear_captures(actor: Actor):
        assert isinstance(actor, ActorMock)
        actor.on_receive__clear_captures()

    def on_receive__senders(actor: Actor) -> List[Address]:
        assert isinstance(actor, ActorMock)
        return actor.on_receive__senders

    def on_receive__messages(actor: Actor) -> List[Message]:
        assert isinstance(actor, ActorMock)
        return actor.on_receive__messages

    assert_should_not_let_actor_receive_any_message_when_stopping(lambda: ActorMock(), stop, on_receive__clear_captures,
                                                                  on_receive__senders, on_receive__messages)


def test_should_call_on_stop_after_actor_raising_process_stop_signal():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    def on_stop__is_called(actor: Actor) -> bool:
        assert isinstance(actor, ActorMock)
        return actor.on_stop__is_called

    assert_should_call_on_stop_after_actor_raising_process_stop_signal(lambda: ActorMock(), stop, on_stop__is_called)


def test_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped(
        lambda: ActorMock(), stop,
    )


def test_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped(
        lambda: ActorMock(), stop,
    )


def test_should_ignore_any_exception_when_running_on_stop():
    def stop(process: ActorProcess, _: Address):
        process.receive(Address("$.someone"), ActorMockStop())

    assert_should_ignore_any_exception_when_running_on_stop(lambda: ActorMock(), stop)
