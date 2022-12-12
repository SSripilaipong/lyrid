import queue
from typing import Dict, List, Callable, SupportsFloat, Tuple

from lyrid.base.actor import Actor
from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.common import IdGenerator, Randomizer
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import MessengerRegisterAddressCompletedMessage, MessengerRegisterAddressMessage, IMessenger
from lyrid.core.node import NodeSpawnProcessCompletedMessage, NodeSpawnProcessMessage
from lyrid.core.process import ProcessFactory, ProcessContext
from lyrid.core.system import SpawnChildMessage, SpawnChildCompleted, SystemSpawnActorCompletedReply, Placement
from ._task import Task, ActorSpawnChildTask


class RootActor(Actor):
    def __init__(self, address: Address, messenger: IMessenger, messenger_address: Address, id_generator: IdGenerator,
                 randomizer: Randomizer, node_addresses: List[Address], reply_queue: queue.Queue,
                 placements: List[Placement]):
        super().__init__(ProcessContext(address, messenger, BackgroundTaskExecutorDummy(), id_generator=id_generator))

        self._reply_queue = reply_queue
        self._messenger_address = messenger_address
        self._id_generator = id_generator
        self._randomizer = randomizer
        self._node_addresses = node_addresses
        self._placements = placements

        self._tasks: Dict[str, Task] = {}

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, NodeSpawnProcessCompletedMessage):
            self._messenger_register_address(sender, message)
        elif isinstance(message, SpawnChildMessage):
            self._process_spawn_child_actor(sender, message)
        elif isinstance(message, MessengerRegisterAddressCompletedMessage):
            self._complete_spawning_actor(sender, message)

    def _messenger_register_address(self, sender: Address, message: NodeSpawnProcessCompletedMessage):
        msg = MessengerRegisterAddressMessage(address=message.process_address,
                                              node_address=sender,
                                              ref_id=message.ref_id)
        self.tell(self._messenger_address, msg)

    def _process_spawn_child_actor(self, sender: Address, message: SpawnChildMessage):
        requester, child_key = sender, message.key
        ref_id = self._id_generator.generate()
        self._tasks[ref_id] = ActorSpawnChildTask(requester=requester, child_key=child_key)

        node = self.choose_placement_node(message.type_)

        self.tell(node, NodeSpawnProcessMessage(
            address=requester.child(child_key), type_=message.type_, ref_id=ref_id,
            initial_message=message.initial_message,
        ))

    def choose_placement_node(self, type_: ProcessFactory) -> Address:
        node = None
        if self._placements:
            for placement in self._placements:
                if placement.match.match(type_):
                    node = placement.policy.get_placement_node()
                    break

        if node is None:
            idx = self._randomizer.randrange(len(self._node_addresses))
            node = self._node_addresses[idx]
        return node

    def _complete_spawning_actor(self, _: Address, message: MessengerRegisterAddressCompletedMessage):
        task = self._tasks.get(message.ref_id, None)
        if isinstance(task, ActorSpawnChildTask):
            self.tell(task.requester, SpawnChildCompleted(key=task.child_key, address=message.address))
            del self._tasks[message.ref_id]
        else:
            self._reply_queue.put(SystemSpawnActorCompletedReply(address=message.address))


class BackgroundTaskExecutorDummy(BackgroundTaskExecutor):
    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        pass

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        pass
