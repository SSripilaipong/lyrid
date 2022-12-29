from dataclasses import dataclass

from lyrid import BackgroundTaskExited
from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


# noinspection DuplicatedCode
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


def test_should_let_actor_receive_background_task_exited_messages():
    actor = ActorMock()
    tester = ActorTester(actor)

    @dataclass
    class MyError(Exception):
        value: str

    def will_fail():
        raise MyError("YOU FAIL!")

    task_id1 = actor.run_in_background(lambda: 123)
    task_id2 = actor.run_in_background(will_fail)

    tester.simulate.run_all_background_tasks()

    assert actor.on_receive__messages == [
        BackgroundTaskExited(task_id1, return_value=123, exception=None),
        BackgroundTaskExited(task_id2, return_value=None, exception=MyError("YOU FAIL!")),
    ] and actor.on_receive__senders == [tester.actor_address, tester.actor_address]


# noinspection DuplicatedCode
def test_should_allow_background_tasks_to_run_without_notifying_actor():
    actor = ActorMock()
    tester = ActorTester(actor)

    func_is_called_with_params = []

    def func(a: int, b: str):
        func_is_called_with_params.append((a, b))

    actor.run_in_background(func, args=(123, "hello"))
    actor.run_in_background(func, args=(456, "world"))

    tester.simulate.run_all_background_tasks(notify_actor=False)

    assert actor.on_receive__messages == [] and actor.on_receive__senders == []
