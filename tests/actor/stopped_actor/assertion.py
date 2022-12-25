from typing import Callable, List

from lyrid import ActorProcess, AbstractActor
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


def assert_handle_stopped_actor(actor_type: Callable[[], AbstractActor],
                                stop: Callable[[ActorProcess, Address], None],
                                on_receive__clear_captures: Callable[[AbstractActor], None],
                                on_receive__senders: Callable[[AbstractActor], List[Address]],
                                on_receive__messages: Callable[[AbstractActor], List[Message]],
                                on_stop__is_called: Callable[[AbstractActor], bool],
                                exception: Exception = None):
    assert_should_send_child_actor_stopped_message_to_supervisor(actor_type, stop, exception=exception)
    assert_should_send_supervisor_force_stop_message_to_spawned_children(actor_type, stop)
    assert_should_send_supervisor_force_stop_message_to_not_stopped_children_only(actor_type, stop)
    assert_should_raise_actor_stopped_signal_to_outside_after_actor_tried_to_stop_and_all_children_are_stopped(
        actor_type, stop)
    assert_should_not_let_actor_receive_any_message_when_stopping(actor_type, stop, on_receive__clear_captures,
                                                                  on_receive__senders, on_receive__messages)
    assert_should_call_on_stop_after_actor_raising_process_stop_signal(actor_type, stop, on_stop__is_called)
    assert_should_send_child_actor_stopped_message_to_supervisor_after_all_active_children_stopped(actor_type, stop,
                                                                                                   exception=exception)
    assert_should_not_send_child_actor_stopped_message_to_supervisor_before_all_active_children_stopped(actor_type,
                                                                                                        stop)
    assert_should_ignore_any_exception_when_running_on_stop(actor_type, stop)
