from lyrid import Address
from lyrid.core.node import NodeSpawnProcessMessage
from lyrid.core.system import Placement, SpawnChildMessage
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.placement_policy import PlacementPolicyMatcherMock, PlacementPolicyMock
from tests.system.actor_dummy import ProcessDummy
from tests.system.util import root_process_message


def test_should_pass_process_type_to_policy_matcher_when_processing_spawn_child_message():
    matcher = PlacementPolicyMatcherMock()
    system = create_actor_system(placements=[Placement(match=matcher, policy=PlacementPolicyMock())],
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", type_=ProcessDummy))

    assert matcher.match__type == ProcessDummy


def test_should_send_node_spawn_process_message_to_the_address_from_policy():
    messenger = MessengerMock()
    policy = PlacementPolicyMock(get_placement_node__return=Address("#node1"))
    system = create_actor_system(messenger=messenger,
                                 placements=[Placement(PlacementPolicyMatcherMock(match__return=True), policy)],
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", type_=ProcessDummy))

    assert messenger.send__receiver == Address("#node1") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)


def test_should_use_node_address_from_first_matched_policy():
    messenger = MessengerMock()
    placements = [
        Placement(
            match=PlacementPolicyMatcherMock(match__return=False),
            policy=PlacementPolicyMock(get_placement_node__return=Address("#node0")),
        ),
        Placement(
            match=PlacementPolicyMatcherMock(match__return=True),
            policy=PlacementPolicyMock(get_placement_node__return=Address("#node1")),
        ),
        Placement(
            match=PlacementPolicyMatcherMock(match__return=True),
            policy=PlacementPolicyMock(get_placement_node__return=Address("#node2")),
        ),
    ]

    # noinspection DuplicatedCode
    system = create_actor_system(messenger=messenger, placements=placements,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    root_process_message(system, sender=Address("$.process"),
                         message=SpawnChildMessage(key="my_child", type_=ProcessDummy))

    assert messenger.send__receiver == Address("#node1") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)
