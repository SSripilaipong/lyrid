from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_run_all_background_tasks():
    actor = ActorMock()
    tester = ActorTester(actor)

    func_is_called_with_params = []

    def func(a: int, b: str):
        func_is_called_with_params.append((a, b))

    actor.run_in_background(func, args=(123, "hello"))
    actor.run_in_background(func, args=(456, "world"))

    tester.simulate.run_all_background_tasks()

    assert func_is_called_with_params == [(123, "hello"), (456, "world")]
