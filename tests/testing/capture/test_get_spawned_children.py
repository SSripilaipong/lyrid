from dataclasses import dataclass

from lyrid import Actor
from lyrid.testing import ActorTester, CapturedSpawnedChild
from tests.mock.actor import ActorMock


@dataclass
class ChildActor(Actor):
    name: str
    value: int


def test_should_return_spawned_child():
    actor = ActorMock()
    tester = ActorTester(actor)

    address = actor.spawn(ChildActor("first", 123))

    assert tester.capture.get_spawned_children() == [
        CapturedSpawnedChild(ChildActor("first", 123), address=address, initial_message=None),
    ]
