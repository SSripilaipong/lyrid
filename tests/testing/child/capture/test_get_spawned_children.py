from lyrid.testing import ActorTester, CapturedSpawnedChild
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.testing.child.child_actor import ChildActor


def test_should_return_spawned_child():
    actor = ActorMock()
    tester = ActorTester(actor)

    address = actor.spawn(ChildActor("first", 123))

    assert tester.capture.get_spawned_children() == [
        CapturedSpawnedChild(ChildActor("first", 123), address=address, initial_message=None),
    ]


def test_should_return_spawned_children_with_initial_message_if_any():
    actor = ActorMock()
    tester = ActorTester(actor)

    address1 = actor.spawn(ChildActor("first", 123), key="first")
    address2 = actor.spawn(ChildActor("second", 456), initial_message=MessageDummy("Start!"))

    assert set(tester.capture.get_spawned_children()) == {
        CapturedSpawnedChild(ChildActor("first", 123), address=address1, initial_message=None),
        CapturedSpawnedChild(ChildActor("second", 456), address=address2, initial_message=MessageDummy("Start!")),
    }


def test_should_allow_filtering_by_address():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.spawn(ChildActor("first1", 123), key="first", initial_message=MessageDummy("Yo"))
    actor.spawn(ChildActor("second", 456), initial_message=MessageDummy("Start!"))
    address = actor.spawn(ChildActor("first2", 456), key="first")

    assert set(tester.capture.get_spawned_children(address=address)) == {
        CapturedSpawnedChild(ChildActor("first1", 123), address=address, initial_message=MessageDummy("Yo")),
        CapturedSpawnedChild(ChildActor("first2", 456), address=address, initial_message=None),
    }
