from dataclasses import dataclass
from typing import Optional

from lyrid import Switch, Message, Actor
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor_process


@dataclass
class MessageA(Message):
    value: int


@dataclass
class MessageB(Message):
    name: str


@dataclass
class MyActor(Actor):
    handle_a__sender: Optional[Address] = None
    handle_a__message: Optional[Message] = None
    handle_b__sender: Optional[Address] = None
    handle_b__message: Optional[Message] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=MessageA)
    def handle_a(self, sender: Address, message: MessageA):
        self.handle_a__sender = sender
        self.handle_a__message = message

    @switch.message(type=MessageB)
    def handle_b(self, sender: Address, message: MessageB):
        self.handle_b__sender = sender
        self.handle_b__message = message


def test_should_call_handle_a():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.from.me"), MessageA(value=123))

    assert actor.handle_a__sender == Address("$.from.me") and actor.handle_a__message == MessageA(value=123)
    assert actor.handle_b__sender is None and actor.handle_b__message is None


def test_should_call_handle_b():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.someone"), MessageB(name="Shane"))

    assert actor.handle_a__sender is None and actor.handle_a__message is None
    assert actor.handle_b__sender == Address("$.someone") and actor.handle_b__message == MessageB(name="Shane")
