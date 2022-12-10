from lyrid import Address
from lyrid.core.system import SpawnChildMessage
from lyrid.system import Placement
from tests.factory.system import create_actor_system
from tests.mock.placement_policy import PlacementPolicyMock, PlacementPolicyMatcherMock
from tests.system.actor_dummy import ProcessDummy
from tests.system.util import root_process_message


def test_should_pass_placement_policy_all_node_addresses_when_creating_actor_system():
    policy1, policy2 = PlacementPolicyMock(), PlacementPolicyMock()

    create_actor_system(
        placement=[Placement(match=PlacementPolicyMatcherMock(), policy=policy1),
                   Placement(match=PlacementPolicyMatcherMock(), policy=policy2)],
        node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")],
    )

    assert policy1.set_node_addresses__addresses == policy2.set_node_addresses__addresses == \
           [Address("#node0"), Address("#node1"), Address("#node2")]


def test_should_pass_process_type_to_policy_matcher_when_processing_spawn_child_message():
    matcher = PlacementPolicyMatcherMock()
    system = create_actor_system(placement=[Placement(match=matcher, policy=PlacementPolicyMock())],
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", type_=ProcessDummy))

    assert matcher.match__type == ProcessDummy
