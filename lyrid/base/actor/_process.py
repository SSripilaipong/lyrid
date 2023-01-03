from contextlib import suppress
from dataclasses import dataclass, field

from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process, ProcessStoppedSignal, ChildStopped, SupervisorForceStop, ProcessContext
from ._abstract import AbstractActor, ActorContext
from ._status import ActorStatus


@dataclass
class ActorProcess(Process):
    _actor: AbstractActor
    _context: ActorContext = field(init=False, compare=False)  # just for type hinting

    @property
    def actor(self) -> AbstractActor:
        return self._actor

    def receive(self, sender: Address, message: Message):
        if isinstance(message, ChildStopped):
            self._context.active_children -= {message.child_address}

        if self._context.status is ActorStatus.ACTIVE:
            self._receive_when_active(sender, message)
        elif self._context.status is ActorStatus.STOPPING:
            self._receive_when_stopping(sender, message)

    def on_receive(self, sender: Address, message: Message):
        self._actor = self._context.next_actor
        self._actor.set_context(self._context)
        self._actor.on_receive(sender, message)
        self._actor = self._context.next_actor

    def on_stop(self):
        self._actor.on_stop()

    def _receive_when_active(self, sender: Address, message: Message):
        if isinstance(message, SupervisorForceStop):
            self._handle_stopping(None)
            return

        try:
            self.on_receive(sender, message)
        except ProcessStoppedSignal:
            self._handle_stopping(None)
        except Exception as e:
            self._handle_stopping(e)

    def _handle_stopping(self, exception: Exception = None):
        with suppress(Exception):
            self.on_stop()
        self._context.status = ActorStatus.STOPPING
        self._context.stopped_message_to_report = ChildStopped(child_address=self._context.address, exception=exception)
        if not self._context.active_children:
            self._context.messenger.send(self._context.address, self._context.address.supervisor(),
                                         self._context.stopped_message_to_report)
            raise ProcessStoppedSignal()
        else:
            for child in self._context.active_children:
                self._context.messenger.send(self._context.address, child, SupervisorForceStop(address=child))

    def _receive_when_stopping(self, _: Address, __: Message):
        if not self._context.active_children:
            if self._context.stopped_message_to_report is not None:
                self._context.messenger.send(self._context.address, self._context.address.supervisor(),
                                             self._context.stopped_message_to_report)
            raise ProcessStoppedSignal()

    def set_context(self, context: ProcessContext):
        self._context = ActorContext(
            context.address, context.messenger, context.background_task_executor, context.id_generator,
            next_actor=self._actor,
        )
        self._actor.set_context(self._context)
