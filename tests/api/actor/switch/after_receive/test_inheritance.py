from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Message, Address
from tests.factory.actor import create_actor_process


class MessageA(Message):
    pass


def test_should_inherit_after_receive_from_parent():
    @use_switch
    @dataclass
    class Parent(Actor):
        after_receive__is_called: bool = False

        @switch.after_receive()
        def after_receive(self):
            self.after_receive__is_called = True

    @use_switch
    class Child(Parent):

        @switch.message(type=MessageA)
        def handle_message_a(self):
            pass

    actor = Child()
    process = create_actor_process(actor)

    process.receive(Address("$"), MessageA())

    assert actor.after_receive__is_called
