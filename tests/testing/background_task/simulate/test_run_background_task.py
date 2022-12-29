from lyrid.testing import ActorTester
from lyrid.testing.background_task import BackgroundTask
from tests.mock.actor import ActorMock


def test_should_run_background_task():
    tester = ActorTester(ActorMock())

    func_is_called_with_params = []

    def func(a: int, b: str):
        func_is_called_with_params.append((a, b))

    tester.simulate.run_background_task(BackgroundTask("TaskId123", func, args=(123, "hello")))

    assert func_is_called_with_params == [(123, "hello")]
