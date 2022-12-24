from typing import Callable, Any, Type

from lyrid.base import ActorSystemBase
from lyrid.core.process import Process
from tests.system.actor_placement._assertion import assert_pass_process_type_to_policy_matcher, \
    assert_send_node_spawn_process_message_to_the_address_from_policy, \
    assert_use_node_address_from_first_matched_policy, assert_use_random_node_when_no_matched_policy


def assert_handle_placement_like_when_spawning_child_process(
        spawn_process: Callable[[ActorSystemBase], Any], type_: Type[Process],
):
    assert_pass_process_type_to_policy_matcher(spawn_process, type_)
    assert_send_node_spawn_process_message_to_the_address_from_policy(spawn_process)
    assert_use_node_address_from_first_matched_policy(spawn_process)
    assert_use_random_node_when_no_matched_policy(spawn_process)
