from dataclasses import dataclass

from lyrid import BackgroundTaskExited
from lyrid.testing import ActorTester
from lyrid.testing.background_task import BackgroundTask
from tests.mock.actor import ActorMock


def test_should_run_background_task():
    tester = ActorTester(ActorMock())

    func_is_called_with_params = []

    def func(a: int, b: str):
        func_is_called_with_params.append((a, b))

    tester.simulate.run_background_task(BackgroundTask("", func, args=(123, "hello")))

    assert func_is_called_with_params == [(123, "hello")]


def test_should_let_actor_receive_background_task_exited_message_with_return_value():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.run_background_task(BackgroundTask("TaskId123", lambda: 999))

    assert actor.on_receive__messages == [BackgroundTaskExited("TaskId123", return_value=999, exception=None)] and \
           actor.on_receive__senders == [tester.actor_address]


def test_should_let_actor_receive_background_task_exited_message_with_exception_if_occurred():
    actor = ActorMock()
    tester = ActorTester(actor)

    @dataclass
    class MyError(Exception):
        value: str

    def will_fail():
        raise MyError("Boom!")

    tester.simulate.run_background_task(BackgroundTask("TaskId123", will_fail))

    assert actor.on_receive__messages == [
        BackgroundTaskExited("TaskId123", return_value=None, exception=MyError("Boom!")),
    ] and actor.on_receive__senders == [tester.actor_address]


def test_should_allow_background_task_to_run_without_notifying_actor_when_exited():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.run_background_task(BackgroundTask("", lambda: None), notify_actor=False)

    assert actor.on_receive__messages == [] and actor.on_receive__senders == []
