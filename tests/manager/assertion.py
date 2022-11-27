from tests.manager._assertion import (
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor,
    assert_start_task_scheduler_when_receive_processor_start_command,
    assert_stop_task_scheduler_when_receive_processor_stop_command,
    assert_schedule_actor_task_when_handling_actor_message_sending_command,
)
from tests.manager.spawn_actor.assertion import \
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message, \
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command, assert_reply_spawn_actor_completed_message
from tests.manager.stopped_actor.assertion import \
    assert_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message, \
    assert_send_child_actor_stopped_message
from tests.manager.typing import ManagerFactory


def assert_have_all_manager_behaviors(
        create_manager: ManagerFactory,
):
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor(
        create_manager,
    )
    assert_start_task_scheduler_when_receive_processor_start_command(create_manager)
    assert_stop_task_scheduler_when_receive_processor_stop_command(create_manager)
    assert_schedule_actor_task_when_handling_actor_message_sending_command(create_manager)
    assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message(create_manager)
    assert_register_actor_in_scheduler_when_handling_spawn_actor_command(create_manager)
    assert_reply_spawn_actor_completed_message(create_manager)
    assert_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message(create_manager)
    assert_send_child_actor_stopped_message(create_manager)
