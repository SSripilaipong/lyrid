from lyrid.testing import ActorTester
from lyrid.testing.background_task import BackgroundTask
from tests.mock.actor import ActorMock


def test_should_return_background_task():
    actor = ActorMock()
    tester = ActorTester(actor)

    def func(a: int, b: str):
        pass

    task_id = actor.run_in_background(func, args=(123, "hello"))

    assert tester.capture.get_background_tasks() == [BackgroundTask(task_id, func, args=(123, "hello"))]
