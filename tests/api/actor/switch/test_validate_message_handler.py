from dataclasses import dataclass
from typing import Optional

from pytest import raises

from lyrid import Switch, Message, Address, Actor
from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_annotated_as_type_error
from tests.factory.actor import create_actor_process


class CallHandleSenderOnly(Message):
    pass


@dataclass
class CallHandleMessageOnly(Message):
    val: int


@dataclass
class MyActor(Actor):
    handle_sender_only__sender: Optional[Address] = None
    handle_message_only__message: Optional[Message] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=CallHandleSenderOnly)
    def handle_sender_only(self, sender: Address):
        self.handle_sender_only__sender = sender

    @switch.message(type=CallHandleMessageOnly)
    def handle_message_only(self, message: CallHandleMessageOnly):
        self.handle_message_only__message = message


def test_should_allow_handler_with_sender_parameter_only():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.someone"), CallHandleSenderOnly())

    assert actor.handle_sender_only__sender == Address("$.someone")


def test_should_allow_handler_with_message_parameter_only():
    actor = MyActor()
    process = create_actor_process(actor)

    process.receive(Address("$.someone"), CallHandleMessageOnly(123))

    assert actor.handle_message_only__message == CallHandleMessageOnly(123)


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with raises(TypeError) as e:
        class A(Actor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.message(type=Message)
            def func(self, aaa: Address):
                pass

    assert str(e.value) == str(invalid_argument_for_method_error('aaa', 'func'))


def test_should_raise_type_error_when_sender_argument_is_specified_with_wrong_type_annotation():
    with raises(TypeError) as e:
        class A(Actor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.message(type=Message)
            def my_func(self, sender: int, message: Message):
                pass

    assert str(e.value) == str(argument_in_method_must_be_annotated_as_type_error("sender", "my_func", "Address"))


def test_should_raise_type_error_when_message_argument_is_specified_with_wrong_type_annotation():
    class M1(Message):
        pass

    class M2(Message):
        pass

    with raises(TypeError) as e:
        class A(Actor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.message(type=M1)
            def my_func_2(self, sender: Address, message: M2):
                pass

    assert str(e.value) == str(argument_in_method_must_be_annotated_as_type_error("message", "my_func_2", "M1"))
