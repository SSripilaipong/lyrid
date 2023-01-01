from dataclasses import dataclass

import pytest

from lyrid import use_switch, Actor, switch, Address, SpawnChildCompleted
from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error
from tests.factory.actor import create_actor_process
from tests.mock.actor import ActorMock


def test_should_allow_handler_without_parameters():
    @use_switch
    @dataclass
    class MyActor(Actor):
        handle_child_spawned__is_called: bool = False

        @switch.child_spawned()
        def handle_child_spawned(self):
            self.handle_child_spawned__is_called = True

    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.a"))
    child_address = actor.spawn(ActorMock(), key="b")

    process.receive(Address("$"), SpawnChildCompleted(key="b", address=child_address))

    assert actor.handle_child_spawned__is_called


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with pytest.raises(TypeError) as e:
        @use_switch
        class A(Actor):
            @switch.child_spawned()
            def this_handler(self, x: Address):
                pass

    assert str(e.value) == str(invalid_argument_for_method_error('x', 'this_handler'))
