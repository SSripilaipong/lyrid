from lyrid.core.messenger import Node
from tests.factory.system import create_actor_system
from tests.node.assertion import assert_have_all_manager_behaviors


def test_should_be_a_manager():
    assert isinstance(create_actor_system(), Node)


def test_should_have_behaviors_of_a_manager():
    assert_have_all_manager_behaviors(create_actor_system)
