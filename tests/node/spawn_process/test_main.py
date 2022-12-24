from tests.factory.node import create_process_managing_node
from tests.node.spawn_process.assertion import (
    assert_let_processor_process_spawn_process_command_when_handle_node_spawn_process_message,
    assert_register_process_in_scheduler_when_handling_spawn_actor_command,
    assert_reply_spawn_process_completed_message, assert_set_context_to_process,
)


def test_should_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message():
    assert_let_processor_process_spawn_process_command_when_handle_node_spawn_process_message(
        create_process_managing_node)


def test_set_context_to_process():
    assert_set_context_to_process(create_process_managing_node)


def test_should_register_actor_in_scheduler_when_handling_spawn_actor_command():
    assert_register_process_in_scheduler_when_handling_spawn_actor_command(create_process_managing_node)


def test_should_reply_spawn_actor_completed_message():
    assert_reply_spawn_process_completed_message(create_process_managing_node)
