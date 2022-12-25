from dataclasses import dataclass
from typing import Optional

from lyrid import Message, Actor, switch, use_switch
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor_process


@dataclass
class MessageA(Message):
    value: int


@dataclass
class MessageB(Message):
    name: str


@dataclass
class MessageC(Message):
    pass


# noinspection DuplicatedCode
@dataclass
class Base(Actor):
    handle_a__sender: Optional[Address] = None
    handle_a__message: Optional[Message] = None
    base_handle_c__sender: Optional[Address] = None
    base_handle_c__message: Optional[Message] = None

    @switch.message(type=MessageA)
    def handle_a(self, sender: Address, message: MessageA):
        self.handle_a__sender = sender
        self.handle_a__message = message

    @switch.message(type=MessageC)
    def handle_c(self, sender: Address, message: MessageC):
        self.base_handle_c__sender = sender
        self.base_handle_c__message = message


# noinspection DuplicatedCode
@use_switch
@dataclass
class MyActor(Base):
    handle_b__sender: Optional[Address] = None
    handle_b__message: Optional[Message] = None
    my_handle_c__sender: Optional[Address] = None
    my_handle_c__message: Optional[Message] = None

    @switch.message(type=MessageB)
    def handle_b(self, sender: Address, message: MessageB):
        self.handle_b__sender = sender
        self.handle_b__message = message

    @switch.message(type=MessageC)
    def handle_c(self, sender: Address, message: MessageC):
        self.my_handle_c__sender = sender
        self.my_handle_c__message = message


def test_should_call_handle_b():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.from.me"), MessageB("abc"))

    assert actor.handle_b__sender == Address("$.from.me") and actor.handle_b__message == MessageB("abc")


def test_should_call_handle_a():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.someone"), MessageA(123))

    assert actor.handle_a__sender == Address("$.someone") and actor.handle_a__message == MessageA(123)


def test_should_call_handle_c_from_my_actor():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.me"), MessageC())

    assert actor.my_handle_c__sender == Address("$.me") and actor.my_handle_c__message == MessageC()
