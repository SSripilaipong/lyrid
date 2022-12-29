from dataclasses import dataclass

import pytest

from lyrid import BackgroundTaskExited
from lyrid.testing import ActorTester
from lyrid.testing.error_message import specifying_both_return_value_and_exception_is_not_allowed
from tests.mock.actor import ActorMock


@dataclass
class MyError(Exception):
    value: str


def test_should_let_actor_receive_background_task_exited_message():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.background_task_exit("TaskXXX")

    assert actor.on_receive__messages == [BackgroundTaskExited("TaskXXX", return_value=None, exception=None)] and \
           actor.on_receive__senders == [tester.actor_address]


def test_should_let_actor_receive_background_task_exited_message_with_return_value():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.background_task_exit("TaskXXX", return_value=123)

    assert actor.on_receive__messages == [BackgroundTaskExited("TaskXXX", return_value=123, exception=None)] and \
           actor.on_receive__senders == [tester.actor_address]


def test_should_let_actor_receive_background_task_exited_message_with_exception():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.background_task_exit("TaskXXX", exception=MyError("!!!"))

    assert actor.on_receive__messages == [
        BackgroundTaskExited("TaskXXX", return_value=None, exception=MyError("!!!")),
    ] and actor.on_receive__senders == [tester.actor_address]


def test_should_raise_type_error_when_specifying_both_return_value_and_exception():
    actor = ActorMock()
    tester = ActorTester(actor)

    with pytest.raises(TypeError) as e:
        tester.simulate.background_task_exit("TaskXXX", return_value=123, exception=MyError(""))

    assert str(e.value) == specifying_both_return_value_and_exception_is_not_allowed
