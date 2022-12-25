from typing import List

from lyrid import ActorProcess, AbstractActor
from lyrid.core.messaging import Address, Message
from tests.actor.actor_mock import WillFail, FailDummy
from tests.actor.stopped_actor.assertion import assert_handle_stopped_actor


class MyError(Exception):
    pass


def test_should_handle_stopped_actor_when_fails_on_receive():
    my_error = MyError()

    def stop(actor: ActorProcess, address: Address):
        actor.receive(address.supervisor(), FailDummy(exception=my_error))

    # noinspection DuplicatedCode
    def on_receive__clear_captures(actor: AbstractActor):
        assert isinstance(actor, WillFail)
        actor.on_receive__clear_captures()

    def on_receive__senders(actor: AbstractActor) -> List[Address]:
        assert isinstance(actor, WillFail)
        return actor.on_receive__senders

    def on_receive__messages(actor: AbstractActor) -> List[Message]:
        assert isinstance(actor, WillFail)
        return actor.on_receive__messages

    def on_stop__is_called(actor: AbstractActor) -> bool:
        assert isinstance(actor, WillFail)
        return actor.on_stop__is_called

    assert_handle_stopped_actor(lambda: WillFail(), stop, on_receive__clear_captures, on_receive__senders,
                                on_receive__messages,
                                on_stop__is_called, exception=my_error)
