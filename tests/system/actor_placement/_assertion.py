from typing import Callable, Any, Type

from lyrid import Address
from lyrid.base import ActorSystemBase
from lyrid.core.node import NodeSpawnProcessMessage
from lyrid.core.process import Process
from lyrid.core.system import Placement
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.placement_policy import PlacementPolicyMatcherMock, PlacementPolicyMock
from tests.mock.randomizer import RandomizerMock


def assert_pass_process_type_to_policy_matcher(spawn_process: Callable[[ActorSystemBase], Any], type_: Type[Process]):
    matcher = PlacementPolicyMatcherMock()
    system = create_actor_system(placements=[Placement(match=matcher, policy=PlacementPolicyMock())],
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    spawn_process(system)

    assert matcher.match__type == type_


def assert_send_node_spawn_process_message_to_the_address_from_policy(spawn_process: Callable[[ActorSystemBase], Any]):
    messenger = MessengerMock()
    policy = PlacementPolicyMock(get_placement_node__return=Address("#node1"))
    system = create_actor_system(messenger=messenger,
                                 placements=[Placement(PlacementPolicyMatcherMock(match__return=True), policy)],
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    spawn_process(system)

    assert messenger.send__receiver == Address("#node1") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)


def assert_use_node_address_from_first_matched_policy(spawn_process: Callable[[ActorSystemBase], Any]):
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

    spawn_process(system)

    assert messenger.send__receiver == Address("#node1") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)


def assert_use_random_node_when_no_matched_policy(spawn_process: Callable[[ActorSystemBase], Any]):
    messenger = MessengerMock()
    placements = [
        Placement(
            match=PlacementPolicyMatcherMock(match__return=False),
            policy=PlacementPolicyMock(get_placement_node__return=Address("#node0")),
        ),
        Placement(
            match=PlacementPolicyMatcherMock(match__return=False),
            policy=PlacementPolicyMock(get_placement_node__return=Address("#node1")),
        ),
    ]
    randomizer = RandomizerMock(randrange__return=2)

    system = create_actor_system(messenger=messenger, placements=placements, randomizer=randomizer,
                                 node_addresses=[Address("#node0"), Address("#node1"), Address("#node2")])

    spawn_process(system)

    assert messenger.send__receiver == Address("#node2") and \
           isinstance(messenger.send__message, NodeSpawnProcessMessage)
