from lyrid import Address
from lyrid.base import ActorSystemBase
from lyrid.core.process import ProcessFactory
from lyrid.core.system import SpawnChildMessage
from tests.system.actor_placement._assertion import assert_pass_process_type_to_policy_matcher, \
    assert_send_node_spawn_process_message_to_the_address_from_policy, \
    assert_use_node_address_from_first_matched_policy, assert_use_random_node_when_no_matched_policy
from tests.system.process_dummy import ProcessDummyWithContext
from tests.system.util import root_process_message


def test_should_pass_process_type_to_policy_matcher_when_processing_spawn_child_message():
    assert_pass_process_type_to_policy_matcher(spawn_child_process_with_type(ProcessDummyWithContext),
                                               ProcessDummyWithContext)


def test_should_send_node_spawn_process_message_to_the_address_from_policy():
    assert_send_node_spawn_process_message_to_the_address_from_policy(spawn_child_process)


def test_should_use_node_address_from_first_matched_policy():
    assert_use_node_address_from_first_matched_policy(spawn_child_process)


def test_should_use_random_node_when_no_matched_policy():
    assert_use_random_node_when_no_matched_policy(spawn_child_process)


def spawn_child_process(system: ActorSystemBase):
    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", type_=ProcessDummyWithContext, process=None))


def spawn_child_process_with_type(type_: ProcessFactory):
    def spawn(system: ActorSystemBase):
        root_process_message(system, sender=Address("$.process"),
                             message=SpawnChildMessage(key="my_child", type_=type_, process=None))

    return spawn
