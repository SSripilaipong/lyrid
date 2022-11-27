import queue
from typing import Dict, List

from lyrid.base._actor import ActorBase
from lyrid.core.common import IIdGenerator
from lyrid.core.manager import ManagerSpawnActorCompletedMessage, ManagerSpawnActorMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import MessengerRegisterAddressCompletedMessage, MessengerRegisterAddressMessage, IMessenger
from lyrid.core.system import SpawnChildMessage, SpawnChildCompletedMessage, SystemSpawnActorCompletedReply
from ._task import Task, ActorSpawnChildTask


class RootActor(ActorBase):
    def __init__(self, address: Address, messenger: IMessenger, messenger_address: Address, id_generator: IIdGenerator,
                 manager_addresses: List[Address], reply_queue: queue.Queue):
        super().__init__(address, messenger)

        self._reply_queue = reply_queue
        self._messenger_address = messenger_address
        self._id_generator = id_generator
        self._manager_addresses = manager_addresses

        self._tasks: Dict[str, Task] = {}

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, ManagerSpawnActorCompletedMessage):
            self._messenger_register_address(sender, message)
        elif isinstance(message, SpawnChildMessage):
            self._actor_spawn_child_actor(sender, message)
        elif isinstance(message, MessengerRegisterAddressCompletedMessage):
            self._complete_spawning_actor(sender, message)

    def _messenger_register_address(self, sender: Address, message: ManagerSpawnActorCompletedMessage):
        msg = MessengerRegisterAddressMessage(address=message.actor_address,
                                              manager_address=sender,
                                              ref_id=message.ref_id)
        self.tell(self._messenger_address, msg)

    def _actor_spawn_child_actor(self, sender: Address, message: SpawnChildMessage):
        requester, child_key = sender, message.key
        ref_id = self._id_generator.generate()
        self._tasks[ref_id] = ActorSpawnChildTask(requester=requester, child_key=child_key)

        self.tell(self._manager_addresses[0], ManagerSpawnActorMessage(
            address=requester.child(child_key), type_=message.type_, ref_id=ref_id,
        ))

    def _complete_spawning_actor(self, _: Address, message: MessengerRegisterAddressCompletedMessage):
        task = self._tasks.get(message.ref_id, None)
        if isinstance(task, ActorSpawnChildTask):
            self.tell(task.requester, SpawnChildCompletedMessage(key=task.child_key, address=message.address))
            del self._tasks[message.ref_id]
        else:
            self._reply_queue.put(SystemSpawnActorCompletedReply(address=message.address))