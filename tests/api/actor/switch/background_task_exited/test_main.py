from dataclasses import dataclass
from typing import Optional, Any

from lyrid import use_switch, Actor, switch, BackgroundTaskExited
from tests.factory.actor import create_actor_process
from tests.mock.actor import ActorMock


class MyException(Exception):
    pass


@use_switch
@dataclass
class MyActor(Actor):
    handle_task_exited__task_id: Optional[str] = None
    handle_task_exited__result: Optional[Any] = None
    handle_task_exited_with_exception__task_id: Optional[str] = None
    handle_task_exited_with_exception__exception: Optional[Exception] = None

    @switch.background_task_exited(exception=None)
    def handle_task_exited(self, task_id: str, result: Any):
        self.handle_task_exited__task_id = task_id
        self.handle_task_exited__result = result

    @switch.background_task_exited(exception=MyException)
    def handle_task_exited_with_exception(self, task_id: str, exception: MyException):
        self.handle_task_exited_with_exception__task_id = task_id
        self.handle_task_exited_with_exception__exception = exception


def test_should_call_handle_task_exited():
    actor = MyActor()
    process = create_actor_process(actor)

    child_address = actor.spawn(ActorMock(), key="child")
    process.receive(child_address, BackgroundTaskExited(task_id="Id123", return_value="My result"))

    assert actor.handle_task_exited__task_id == "Id123" and actor.handle_task_exited__result == "My result"
    assert actor.handle_task_exited_with_exception__task_id is None and \
           actor.handle_task_exited_with_exception__exception is None
