from contextlib import suppress
from typing import List

from lyrid import ActorProcess, Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.process import SupervisorForceStop, ProcessStoppedSignal
from tests.actor.stopped_actor.assertion import assert_handle_stopped_actor
from tests.factory.actor import create_actor_process
from tests.mock.actor import ActorMock, ActorMockStop


def test_should_handle_stopped_actor_when_receive_supervisor_force_stop():
    def stop(process: ActorProcess, address: Address):
        process.receive(address.supervisor(), SupervisorForceStop(address=address))

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

    assert_handle_stopped_actor(ActorMock, stop, on_receive__clear_captures, on_receive__senders, on_receive__messages,
                                on_stop__is_called)


def test_should_not_call_on_stop_twice():
    actor = ActorMock()
    process = create_actor_process(actor, address=Address("$.supervisor.my_actor"))

    with suppress(ProcessStoppedSignal):
        process.receive(Address("$"), ActorMockStop())
    actor.on_stop__is_called = False  # reset flag

    with suppress(ProcessStoppedSignal):
        process.receive(Address("$.supervisor"), SupervisorForceStop(address=Address("$.supervisor.my_actor")))

    assert not actor.on_stop__is_called


def test_should_not_let_actor_receive_supervisor_force_stop_message_in_case_the_actor_has_child():
    actor = ActorMock()

    process = create_actor_process(actor, address=Address("$.supervisor.my_actor"))

    actor.spawn(ActorMock())
    with suppress(ProcessStoppedSignal):
        process.receive(Address("$.supervisor"), SupervisorForceStop(address=Address("$.supervisor.my_actor")))

    assert actor.on_receive__messages == [] and actor.on_receive__senders == []
