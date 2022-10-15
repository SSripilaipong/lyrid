from tests.assert_manager import (
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor,
    assert_start_task_scheduler_when_receive_processor_start_command,
    assert_stop_task_scheduler_when_receive_processor_stop_command,
    assert_schedule_actor_task_when_handling_actor_message_sending_command,
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message,
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command,
)
from tests.factory.manager import create_manager


def test_should_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor():
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor(
        create_manager,
    )


def test_should_start_task_scheduler_when_receive_processor_start_command():
    assert_start_task_scheduler_when_receive_processor_start_command(create_manager)


def test_should_stop_task_scheduler_when_receive_processor_stop_command():
    assert_stop_task_scheduler_when_receive_processor_stop_command(create_manager)


def test_should_schedule_actor_task_when_handling_actor_message_sending_command():
    assert_schedule_actor_task_when_handling_actor_message_sending_command(create_manager)


def test_should_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message():
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message(create_manager)


def test_should_register_actor_in_scheduler_when_handling_spawn_actor_command():
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command(create_manager)
