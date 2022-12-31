from dataclasses import dataclass
from typing import Optional

from lyrid import Actor, switch, use_switch, ChildStopped
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor_process
from tests.mock.actor import ActorMock


@dataclass
class MyException(Exception):
    value: str


@use_switch
@dataclass
class MyActor(Actor):
    handle_child_stopped__address: Optional[Address] = None
    handle_child_stopped_with_exception__address: Optional[Address] = None
    handle_child_stopped_with_exception__exception: Optional[Exception] = None

    @switch.child_stopped(exception=None)
    def handle_child_stopped(self, address: Address):
        self.handle_child_stopped__address = address

    @switch.child_stopped(exception=MyException)
    def handle_child_stopped_with_exception(self, address: Address, exception: MyException):
        self.handle_child_stopped_with_exception__address = address
        self.handle_child_stopped_with_exception__exception = exception


def test_should_call_handle_child_stopped():
    actor = MyActor()
    process = create_actor_process(actor, address=Address("$.me"))

    child_address = actor.spawn(ActorMock(), key="child")
    process.receive(child_address, ChildStopped(child_address=child_address))

    assert actor.handle_child_stopped__address == Address("$.me.child")
    assert actor.handle_child_stopped_with_exception__address is None
