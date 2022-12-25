from abc import ABC, abstractmethod
from typing import SupportsFloat, Optional, Callable, Tuple

from lyrid.core.messaging import Address, Message, Reply
from lyrid.core.process import Process, ProcessStoppedSignal
from lyrid.core.system import SpawnChildMessage
from ._context import ActorContext


class AbstractActor(ABC):
    _context: ActorContext

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass

    def on_stop(self):
        pass

    @property
    def context(self) -> ActorContext:
        return self._context

    def set_context(self, context: ActorContext):
        self._context = context

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

    def stop(self):
        raise ProcessStoppedSignal()
