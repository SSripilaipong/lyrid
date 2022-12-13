from typing import Optional

from lyrid import StatefulActor, Switch, Message, Address
from tests.factory.actor import create_actor


class CallHandleSenderOnly(Message):
    pass


class MyActor(StatefulActor):
    handle_sender_only__sender: Optional[Address] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=CallHandleSenderOnly)
    def handle_sender_only(self, sender: Address):
        self.handle_sender_only__sender = sender


def test_should_allow_handler_with_sender_parameter_only():
    actor = create_actor(MyActor)

    actor.receive(Address("$.someone"), CallHandleSenderOnly())

    assert actor.handle_sender_only__sender == Address("$.someone")
