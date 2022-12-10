from lyrid import Address
from lyrid.system import Placement, MatchAny
from tests.factory.system import create_actor_system
from tests.mock.placement_policy import PlacementPolicyMock


def test_should_pass_placement_policy_all_node_addresses_when_creating_actor_system():
    policy1, policy2 = PlacementPolicyMock(), PlacementPolicyMock()

    create_actor_system(
        placement=[Placement(match=MatchAny(), policy=policy1), Placement(match=MatchAny(), policy=policy2)],
        node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")],
    )

    assert policy1.set_node_addresses__addresses == policy2.set_node_addresses__addresses == \
           [Address("#node0"), Address("#node1"), Address("#node2")]
