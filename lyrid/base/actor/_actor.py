from typing import SupportsFloat, Optional, Callable, Tuple

from lyrid.core.messaging import Address, Message, Reply
from lyrid.core.process import ProcessStoppedSignal
from lyrid.core.system import SpawnChildMessage
from ._abstract import AbstractActor
from ._process import ActorProcess


class Actor(AbstractActor):

    def on_receive(self, sender: Address, message: Message):
        pass

    def on_stop(self):
        pass

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

    def spawn(self, actor: 'Actor', *, key: str = None, initial_message: Optional[Message] = None) -> Address:
        key = key or self._context.id_generator.generate()
        process = ActorProcess(actor)
        self._context.messenger.send(self._context.address, self._context.system_address,
                                     SpawnChildMessage(key=key, initial_message=initial_message, process=process))

        addr = self._context.address.child(key)
        self._context.active_children.add(addr)
        return addr

    def run_in_background(self, task: Callable, *, args: Tuple = ()) -> str:
        task_id = self._context.id_generator.generate()
        self._context.background_task_executor.execute(task_id, self.address, task, args=args)
        return task_id

    def stop(self):
        raise ProcessStoppedSignal()

    def become(self, actor: 'Actor'):
        self._context.next_actor = actor
