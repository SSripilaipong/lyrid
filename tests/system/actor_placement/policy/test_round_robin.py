from lyrid import Address
from lyrid.system import RoundRobin


def test_should_return_all_node_addresses_without_repeating_in_any_order_when_getting_node_n_times():
    policy = RoundRobin()
    policy.set_node_addresses([Address("#node0"), Address("#node1"), Address("#node2")])

    assert {policy.get_placement_node(), policy.get_placement_node(), policy.get_placement_node()} == \
           {Address("#node0"), Address("#node1"), Address("#node2")}


def test_should_repeat_the_same_order_again_when_getting_more_than_n_times():
    policy = RoundRobin()
    policy.set_node_addresses([Address("#node0"), Address("#node1"), Address("#node2")])

    assert [policy.get_placement_node(), policy.get_placement_node(), policy.get_placement_node()] == \
           [policy.get_placement_node(), policy.get_placement_node(), policy.get_placement_node()]
