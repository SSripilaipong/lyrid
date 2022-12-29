import pytest

from lyrid import ChildStopped, Address
from lyrid.testing import ActorTester
from lyrid.testing.error_message import key_or_address_of_child_must_be_specified
from tests.mock.actor import ActorMock


def test_should_let_actor_receive_child_stopped_message_using_key():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.child_stop(key="ChildKey123")

    assert actor.on_receive__messages == [
        ChildStopped(tester.actor_address.child("ChildKey123"), exception=None),
    ] and actor.on_receive__senders == [tester.actor_address]


def test_should_let_actor_receive_child_stopped_message_using_address():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.child_stop(address=Address("$.tester.actor.child"))

    assert actor.on_receive__messages == [
        ChildStopped(Address("$.tester.actor.child"), exception=None),
    ] and actor.on_receive__senders == [tester.actor_address]


def test_should_raise_type_error_if_neither_key_nor_address_is_provided():
    tester = ActorTester(ActorMock())

    with pytest.raises(TypeError) as e:
        tester.simulate.child_stop()

    assert str(e.value) == key_or_address_of_child_must_be_specified
