from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_clear_background_tasks():
    actor = ActorMock()
    tester = ActorTester(actor)

    actor.run_in_background(lambda a, b: None, args=(123, "hello"))

    tester.capture.clear_background_tasks()

    assert tester.capture.get_background_tasks() == []
