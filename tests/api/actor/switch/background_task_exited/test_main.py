from dataclasses import dataclass
from email.headerregistry import Address
from typing import Optional, Any

from lyrid import use_switch, Actor, switch, BackgroundTaskExited
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy


@dataclass
class MyException(Exception):
    value: str


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
    process = create_actor_process(actor, address=Address("$.me"))

    process.receive(Address("$.me"), BackgroundTaskExited(task_id="Id123", return_value="My result"))

    assert actor.handle_task_exited__task_id == "Id123" and actor.handle_task_exited__result == "My result"
    assert actor.handle_task_exited_with_exception__task_id is None and \
           actor.handle_task_exited_with_exception__exception is None


def test_should_call_handle_task_exited_with_exception():
    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.me"))

    process.receive(Address("$.me"), BackgroundTaskExited(task_id="Id456", exception=MyException("Boom!")))

    assert actor.handle_task_exited_with_exception__task_id == "Id456" and \
           actor.handle_task_exited_with_exception__exception == MyException("Boom!")
    assert actor.handle_task_exited__task_id is None and actor.handle_task_exited__result is None


def test_should_not_call_handle_task_exited_for_other_message():
    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.me"))

    process.receive(Address("$.me"), MessageDummy("Hey"))

    assert actor.handle_task_exited_with_exception__task_id is None and \
           actor.handle_task_exited_with_exception__exception is None and \
           actor.handle_task_exited__task_id is None and \
           actor.handle_task_exited__result is None
