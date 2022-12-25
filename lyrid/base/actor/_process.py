from abc import ABC, abstractmethod
from contextlib import suppress
from typing import Optional, Callable, Tuple, SupportsFloat

from lyrid.core.messaging import Address, Message, Reply
from lyrid.core.process import Process, ProcessStoppedSignal, ChildStopped, SupervisorForceStop, \
    ProcessContext
from lyrid.core.system import SpawnChildMessage
from ._context import ActorContext
from ._status import ActorStatus


class ActorProcess(Process, ABC):
    _context: ActorContext

    @property
    def address(self) -> Address:
        return self._context.address

    def tell(self, receiver: Address, message: Message, *, delay: SupportsFloat = None):
        if delay is None:
            self._context.messenger.send(self._context.address, receiver, message)
        else:
            self._context.background_task_executor.execute_with_delay(self._context.messenger.send, delay=delay,
                                                                      args=(self._context.address, receiver, message))

    def reply(self, receiver: Address, message: Message, *, ref_id: str):
        self.tell(receiver, Reply(message, ref_id=ref_id))

    def spawn(self, key: str, process: Process, *, initial_message: Optional[Message] = None):
        self._context.messenger.send(self._context.address, self._context.system_address,
                                     SpawnChildMessage(key=key, initial_message=initial_message, process=process))
        self._context.active_children.add(self._context.address.child(key))

    def run_in_background(self, task: Callable, *, args: Tuple = ()) -> str:
        task_id = self._context.id_generator.generate()
        self._context.background_task_executor.execute(task_id, self.address, task, args=args)
        return task_id

    def receive(self, sender: Address, message: Message):
        if isinstance(message, ChildStopped):
            self._context.active_children -= {message.child_address}
        elif isinstance(message, SupervisorForceStop):
            self._handle_stopping(None)

        if self._context.status is ActorStatus.ACTIVE:
            self._receive_when_active(sender, message)
        elif self._context.status is ActorStatus.STOPPING:
            self._receive_when_stopping(sender, message)

    def stop(self):
        raise ProcessStoppedSignal()

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass

    def on_stop(self):
        pass

    def _receive_when_active(self, sender: Address, message: Message):
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
            self.tell(self._context.address.supervisor(), self._context.stopped_message_to_report)
            raise ProcessStoppedSignal()
        else:
            for child in self._context.active_children:
                self.tell(child, SupervisorForceStop(address=child))

    def _receive_when_stopping(self, _: Address, __: Message):
        if not self._context.active_children:
            if self._context.stopped_message_to_report is not None:
                self.tell(self._context.address.supervisor(), self._context.stopped_message_to_report)
            raise ProcessStoppedSignal()

    def set_context(self, context: ProcessContext):
        self._context = ActorContext(
            context.address, context.messenger, context.background_task_executor, context.id_generator,
        )
