from typing import List

from lyrid import ActorProcess, Actor
from lyrid.core.messaging import Address, Message
from tests.actor.stopped_actor.assertion import assert_handle_stopped_actor
from tests.mock.actor import ActorMock, ActorMockFail


class MyError(Exception):
    pass


def test_should_handle_stopped_actor_when_fails_on_receive():
    my_error = MyError()

    def stop(actor: ActorProcess, address: Address):
        actor.receive(address.supervisor(), ActorMockFail(exception=my_error))

    # noinspection DuplicatedCode
    def on_receive__clear_captures(actor: Actor):
        assert isinstance(actor, ActorMock)
        actor.on_receive__clear_captures()

    def on_receive__senders(actor: Actor) -> List[Address]:
        assert isinstance(actor, ActorMock)
        return actor.on_receive__senders

    def on_receive__messages(actor: Actor) -> List[Message]:
        assert isinstance(actor, ActorMock)
        return actor.on_receive__messages

    def on_stop__is_called(actor: Actor) -> bool:
        assert isinstance(actor, ActorMock)
        return actor.on_stop__is_called

    assert_handle_stopped_actor(lambda: ActorMock(), stop, on_receive__clear_captures, on_receive__senders,
                                on_receive__messages,
                                on_stop__is_called, exception=my_error)
