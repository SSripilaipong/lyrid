from dataclasses import dataclass

from lyrid import use_switch, Actor, switch, Address, SpawnChildCompleted
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
