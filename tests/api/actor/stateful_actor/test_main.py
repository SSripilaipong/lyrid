from typing import List

from lyrid import StatefulActor, field
from lyrid.core.messaging import Address, Message
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


class Echo(StatefulActor):
    change_me: str = field(default="No")
    use_default_factory: List[str] = field(default_factory=lambda: ["xxx"])
    sender: Address = field(default=None)

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, MessageDummy):
            self.change_me = message.text
        self.tell(sender, message)


def test_should_have_default_value():
    actor = create_actor(Echo)
    assert actor.use_default_factory == ["xxx"] and actor.change_me == "No" and actor.sender is None


def test_should_still_be_able_to_send_message_via_messenger():
    messenger = MessengerMock()
    actor = create_actor(Echo, address=Address("$.me"), messenger=messenger)

    actor.receive(Address("$.someone"), MessageDummy("HeHe"))

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$.someone") and \
           messenger.send__message == MessageDummy("HeHe")


def test_should_change_prop():
    actor = create_actor(Echo)
    actor.receive(Address("$.from.me"), MessageDummy("CHANGED!"))
    assert actor.change_me == "CHANGED!"
