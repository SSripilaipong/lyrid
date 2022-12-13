from typing import Optional

from lyrid import StatefulActor, Switch, Message, Address, Ask
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
