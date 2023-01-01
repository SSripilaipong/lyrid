from dataclasses import dataclass

from lyrid import use_switch, Actor, switch, Address, BackgroundTaskExited
from tests.factory.actor import create_actor_process


def test_should_allow_handler_with_or_without_parameters():
    @use_switch
    @dataclass
    class MyActor(Actor):
        handler__is_called: bool = True

        @switch.background_task_exited(exception=None)
        def handler(self):
            self.handler__is_called = True

    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.me"))

    process.receive(Address("$.me"), BackgroundTaskExited(task_id="Id123", return_value="My result"))

    assert actor.handler__is_called
