from typing import Optional

from pytest import raises

from lyrid import StatefulActor, Switch, Message, Address, Ask, VanillaActor
from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_included_as_type_error, argument_in_method_must_be_annotated_as_type_error
from tests.factory.actor import create_actor


class CallHandleWithoutMessage(Message):
    pass


class MyActor(StatefulActor):
    handle_without_message__sender: Optional[Address] = None
    handle_without_message__ref_id: Optional[str] = None
    handle_message_only__message: Optional[Message] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.ask(type=CallHandleWithoutMessage)
    def handle_without_message(self, sender: Address, ref_id: str):
        self.handle_without_message__sender = sender
        self.handle_without_message__ref_id = ref_id


def test_should_allow_handler_without_message_argument():
    actor = create_actor(MyActor)

    actor.receive(Address("$.someone"), Ask(CallHandleWithoutMessage(), ref_id="Id123"))

    assert actor.handle_without_message__sender == Address("$.someone") and \
           actor.handle_without_message__ref_id == "Id123"


def test_should_raise_type_error_when_sender_argument_is_missing():
    class M1(Message):
        pass

    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.ask(type=M1)
            def my_func(self, message: M1, ref_id: str):
                pass

    assert str(e.value) == str(argument_in_method_must_be_included_as_type_error("sender", "my_func", "Address"))


def test_should_raise_type_error_when_ref_id_argument_is_missing():
    class M1(Message):
        pass

    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.ask(type=M1)
            def my_func_2(self, message: M1, sender: Address):
                pass

    assert str(e.value) == str(argument_in_method_must_be_included_as_type_error("ref_id", "my_func_2", "str"))


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.ask(type=Message)
            def fn(self, sender: Address, ref_id: str, bb: Message):
                pass

    assert str(e.value) == str(invalid_argument_for_method_error("bb", "fn"))


def test_should_raise_type_error_when_sender_argument_is_specified_with_wrong_type_annotation():
    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.ask(type=Message)
            def fx(self, sender: str, message: Message, ref_id: str):
                pass

    assert str(e.value) == str(argument_in_method_must_be_annotated_as_type_error("sender", "fx", "Address"))


def test_should_raise_type_error_when_message_argument_is_specified_with_wrong_type_annotation():
    class Msg1(Message):
        pass

    class Msg2(Message):
        pass

    with raises(TypeError) as e:
        class A(VanillaActor):
            switch = Switch()
            on_receive = switch.on_receive

            @switch.ask(type=Msg1)
            def my_func(self, sender: Address, message: Msg2, ref_id: str):
                pass

    assert str(e.value) == str(argument_in_method_must_be_annotated_as_type_error("message", "my_func", "Msg1"))
