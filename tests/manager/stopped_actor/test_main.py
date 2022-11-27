from tests.factory.manager import create_manager
from tests.manager.stopped_actor.assertion import \
    assert_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message, \
    assert_send_child_actor_stopped_message


def test_should_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message():
    assert_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message(create_manager)


def test_should_send_child_actor_stopped_message():
    assert_send_child_actor_stopped_message(create_manager)
