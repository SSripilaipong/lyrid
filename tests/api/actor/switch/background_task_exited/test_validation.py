from dataclasses import dataclass

import pytest

from lyrid import use_switch, Actor, switch, Address, BackgroundTaskExited
from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_annotated_as_type_error
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


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with pytest.raises(TypeError) as e:
        @use_switch
        class A(Actor):
            @switch.background_task_exited(exception=None)
            def bg_task_exited(self, abc: str):
                pass

    assert str(e.value) == str(invalid_argument_for_method_error('abc', 'bg_task_exited'))


def test_should_raise_type_error_when_task_id_argument_is_specified_with_wrong_type_annotation():
    with pytest.raises(TypeError) as e:
        @use_switch
        class A(Actor):
            @switch.background_task_exited(exception=None)
            def my_handler(self, task_id: float):
                pass

    assert str(e.value) == str(argument_in_method_must_be_annotated_as_type_error("task_id", "my_handler", "str"))
