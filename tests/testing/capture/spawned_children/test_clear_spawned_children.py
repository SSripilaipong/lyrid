from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock
from tests.testing.capture.spawned_children.test_get_spawned_children import ChildActor


def test_should_clear_spawned_children():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.spawn(ChildActor("first", 123))
    tester.capture.clear_spawned_children()

    assert tester.capture.get_spawned_children() == []
