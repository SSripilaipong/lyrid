from lyrid import ActorBase
from lyrid.core.messenger import Address, Message
from lyrid.message import TextMessage
from tests.actor_factory import create_actor_with_address_and_messenger
from tests.messenger_mock import MessengerMock


def test_should_send_message_via_messenger():
    messenger = MessengerMock()

    class MyActor(ActorBase):

        def receive(self, sender: Address, message: Message):
            self.tell(Address("$.you"), TextMessage("Hello!"))

    actor = create_actor_with_address_and_messenger(MyActor, Address("$.me"), messenger)
    actor.receive(Address("$"), Message())

    assert messenger.send__sender == Address("$.me") and \
           messenger.send__receiver == Address("$.you") and \
           messenger.send__message == TextMessage("Hello!")
