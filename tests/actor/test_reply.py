from lyrid.core.messaging import Address, Reply
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock
from tests.mock.messenger import MessengerMock


def test_should_send_reply_message_via_messenger():
    messenger = MessengerMock()
    actor = ActorMock()
    _ = create_actor_process(actor, address=Address("$.its.me"), messenger=messenger)

    actor.reply(Address("$.to.you"), MessageDummy("Hey!"), ref_id="abc123")

    assert messenger.send__sender == Address("$.its.me") and \
           messenger.send__receiver == Address("$.to.you") and \
           messenger.send__message == Reply(MessageDummy("Hey!"), ref_id="abc123")
