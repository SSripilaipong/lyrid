from typing import List

from lyrid import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.process import SupervisorForceStop
from tests.actor.actor_mock import WillStop
from tests.actor.stopped_actor.assertion import assert_handle_stopped_actor


def test_should_handle_stopped_actor_when_receive_supervisor_force_stop():
    def stop(actor: Actor, address: Address):
        actor.receive(address.supervisor(), SupervisorForceStop(address=address))

    # noinspection DuplicatedCode
    def on_receive__clear_captures(actor: Actor):
        assert isinstance(actor, WillStop)
        actor.on_receive__clear_captures()

    def on_receive__senders(actor: Actor) -> List[Address]:
        assert isinstance(actor, WillStop)
        return actor.on_receive__senders

    def on_receive__messages(actor: Actor) -> List[Message]:
        assert isinstance(actor, WillStop)
        return actor.on_receive__messages

    def on_stop__is_called(actor: Actor) -> bool:
        assert isinstance(actor, WillStop)
        return actor.on_stop__is_called

    assert_handle_stopped_actor(WillStop, stop, on_receive__clear_captures, on_receive__senders, on_receive__messages,
                                on_stop__is_called)
