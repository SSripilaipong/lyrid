from dataclasses import dataclass
from typing import Optional

from lyrid import use_switch, Actor, switch, SpawnChildCompleted, Address
from tests.factory.actor import create_actor_process
from tests.mock.actor import ActorMock


@use_switch
@dataclass
class MyActor(Actor):
    handle_child_spawned__address: Optional[Address] = None

    @switch.child_spawned()
    def handle_child_spawned(self, address: Address):
        self.handle_child_spawned__address = address


def test_should_call_handle_child_spawned():
    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.me"))

    child_address = actor.spawn(ActorMock(), key="child")
    process.receive(Address("$"), SpawnChildCompleted(key="child", address=child_address))

    assert actor.handle_child_spawned__address == Address("$.me.child")
