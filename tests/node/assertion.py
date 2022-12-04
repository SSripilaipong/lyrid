from tests.node._assertion import (
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor,
    assert_start_task_scheduler_when_receive_processor_start_command,
    assert_stop_task_scheduler_when_receive_processor_stop_command,
    assert_schedule_actor_task_when_handling_actor_message_sending_command,
)
from tests.node.spawn_process.assertion import \
    assert_let_processor_process_spawn_process_command_when_handle_node_spawn_process_message, \
    assert_register_process_in_scheduler_when_handling_spawn_actor_command, assert_reply_spawn_process_completed_message
from tests.node.typing import NodeFactory


def assert_have_all_manager_behaviors(
        create_manager: NodeFactory,
):
    assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor(
        create_manager,
    )
    assert_start_task_scheduler_when_receive_processor_start_command(create_manager)
    assert_stop_task_scheduler_when_receive_processor_stop_command(create_manager)
    assert_schedule_actor_task_when_handling_actor_message_sending_command(create_manager)
    assert_let_processor_process_spawn_process_command_when_handle_node_spawn_process_message(create_manager)
    assert_register_process_in_scheduler_when_handling_spawn_actor_command(create_manager)
    assert_reply_spawn_process_completed_message(create_manager)
