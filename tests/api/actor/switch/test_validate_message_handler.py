from dataclasses import dataclass
from typing import Optional

from pytest import raises

from lyrid import StatefulActor, Switch, Message, Address, VanillaActor
from tests.factory.actor import create_actor


class CallHandleSenderOnly(Message):
    pass


@dataclass
class CallHandleMessageOnly(Message):
    val: int


class MyActor(StatefulActor):
    handle_sender_only__sender: Optional[Address] = None
    handle_message_only__message: Optional[Message] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=CallHandleSenderOnly)
    def handle_sender_only(self, sender: Address):
        self.handle_sender_only__sender = sender

    @switch.message(type=CallHandleMessageOnly)
    def handle_message_only(self, message: Message):
        self.handle_message_only__message = message


def test_should_allow_handler_with_sender_parameter_only():
    actor = create_actor(MyActor)

    actor.receive(Address("$.someone"), CallHandleSenderOnly())

    assert actor.handle_sender_only__sender == Address("$.someone")


def test_should_allow_handler_with_message_parameter_only():
    actor = create_actor(MyActor)

    actor.receive(Address("$.someone"), CallHandleMessageOnly(123))

    assert actor.handle_message_only__message == CallHandleMessageOnly(123)


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.message(type=Message)
            def func(self, aaa: Address):
                pass

    assert str(e.value) == "'aaa' is an invalid argument for method 'func'"
