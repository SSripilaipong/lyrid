from tests.factory.manager import create_manager
from tests.manager.spawn_actor.assertion import (
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message,
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command, assert_reply_spawn_actor_completed_message,
)


def test_should_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message():
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message(create_manager)


def test_should_register_actor_in_scheduler_when_handling_spawn_actor_command():
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command(create_manager)


def test_should_reply_spawn_actor_completed_message():
    assert_reply_spawn_actor_completed_message(create_manager)
