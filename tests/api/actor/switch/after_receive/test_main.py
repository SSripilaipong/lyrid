from dataclasses import dataclass
from email.headerregistry import Address

from lyrid import use_switch, Actor, switch, Message
from tests.factory.actor import create_actor_process


@dataclass
class MessageA(Message):
    value: str


@dataclass
class MessageB(Message):
    value: str


@use_switch
@dataclass
class MyActor(Actor):
    after_receive__is_called: bool = False

    @switch.message(type=MessageA)
    def handle_a(self):
        pass

    @switch.after_receive()
    def after_receive(self):
        self.after_receive__is_called = True


def test_should_call_after_receive():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$"), MessageA("Hey"))

    assert actor.after_receive__is_called


def test_should_not_call_if_not_received():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$"), MessageB("Ignore this"))

    assert not actor.after_receive__is_called
