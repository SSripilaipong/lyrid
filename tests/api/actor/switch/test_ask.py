from dataclasses import dataclass
from typing import Optional

from lyrid import Message, Ask, Actor, switch, use_switch
from lyrid.core.messaging import Address
from tests.factory.actor import create_actor_process


@dataclass
class QuestionA(Message):
    value: int


@dataclass
class QuestionB(Message):
    name: str


@use_switch
@dataclass
class MyActor(Actor):
    handle_ask_a__sender: Optional[Address] = None
    handle_ask_a__message: Optional[Message] = None
    handle_ask_a__ref_id: Optional[str] = None

    handle_ask_b__sender: Optional[Address] = None
    handle_ask_b__message: Optional[Message] = None
    handle_ask_b__ref_id: Optional[str] = None

    # switch = Switch()
    # on_receive = switch.on_receive
    #
    @switch.ask(type=QuestionA)
    def handle_ask_a(self, sender: Address, message: QuestionA, ref_id: str):
        self.handle_ask_a__sender = sender
        self.handle_ask_a__ref_id = ref_id
        self.handle_ask_a__message = message

    @switch.ask(type=QuestionB)
    def handle_ask_b(self, sender: Address, message: QuestionB, ref_id: str):
        self.handle_ask_b__sender = sender
        self.handle_ask_b__ref_id = ref_id
        self.handle_ask_b__message = message


def test_should_call_handle_ask_a():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.from.me"), Ask(QuestionA(value=123), ref_id="Q1"))

    assert actor.handle_ask_a__sender == Address("$.from.me") and \
           actor.handle_ask_a__message == QuestionA(value=123) and \
           actor.handle_ask_a__ref_id == "Q1"
    assert actor.handle_ask_b__sender is actor.handle_ask_b__message is actor.handle_ask_b__ref_id is None


def test_should_call_handle_ask_b():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.someone"), Ask(QuestionB(name="Shane"), ref_id="Q2"))

    assert actor.handle_ask_a__sender is actor.handle_ask_a__message is actor.handle_ask_a__ref_id is None
    assert actor.handle_ask_b__sender == Address("$.someone") and \
           actor.handle_ask_b__message == QuestionB(name="Shane") and \
           actor.handle_ask_b__ref_id == "Q2"
