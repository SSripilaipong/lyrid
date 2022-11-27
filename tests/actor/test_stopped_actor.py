import pytest

from lyrid.core.actor import ActorStoppedSignal, ChildActorStopped
from lyrid.core.messaging import Address
from tests.actor.actor_mock import WillStop
from tests.factory.actor import create_actor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock


def test_should_send_child_actor_stopped_message_to_supervisor():
    messenger = MessengerMock()
    actor = create_actor(WillStop, address=Address("$.my_supervisor.me"), messenger=messenger)

    with pytest.raises(ActorStoppedSignal):
        actor.receive(Address("$.someone"), MessageDummy("STOPP"))

    assert messenger.send__sender == Address("$.my_supervisor.me") and \
           messenger.send__receiver == Address("$.my_supervisor") and \
           messenger.send__message == ChildActorStopped(child_address=Address("$.my_supervisor.me"))
