from lyrid.core.messenger import IManager
from tests.factory.system import create_actor_system
from tests.manager.assertion import assert_have_all_manager_behaviors


def test_should_be_a_manager():
    assert isinstance(create_actor_system(), IManager)


def test_should_have_behaviors_of_a_manager():
    assert_have_all_manager_behaviors(create_actor_system)
