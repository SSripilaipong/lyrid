import queue
from typing import List, Optional

from lyrid.base import ProcessManagingNode
from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.command_processing_loop import CommandProcessingLoop, Command
from lyrid.core.common import IdGenerator, Randomizer
from lyrid.core.messaging import Address, Message, Ask, Reply
from lyrid.core.messenger import IMessenger
from lyrid.core.node import TaskScheduler, NodeSpawnProcessMessage, MessageHandlingCommand
from lyrid.core.process import ProcessFactory
from lyrid.core.system import SystemSpawnActorCommand, SystemSpawnActorCompletedReply, ActorReplyAskCommand, \
    ActorAskReply, Placement, SystemAskCommand
from ._root import RootActor


class ActorSystemBase(ProcessManagingNode):
    def __init__(self, scheduler: TaskScheduler, processor: CommandProcessingLoop, messenger: IMessenger,
                 placements: List[Placement], node_addresses: List[Address], root_address: Address, address: Address,
                 messenger_address: Address, reply_queue: queue.Queue, id_generator: IdGenerator,
                 randomizer: Randomizer, background_task_executor: BackgroundTaskExecutor,
                 processors: List[CommandProcessingLoop] = None):
        super().__init__(address=address, scheduler=scheduler, processor=processor, messenger=messenger,
                         background_task_executor=background_task_executor, id_generator=id_generator)

        self._root_address = root_address
        self._messenger = messenger
        self._node_addresses = node_addresses
        self._reply_queue = reply_queue
        self._id_generator = id_generator
        self._randomizer = randomizer
        self._processors = processors or []

        for p in placements:
            p.policy.set_node_addresses(self._node_addresses)
        self._placements = placements

        self._root = RootActor(root_address, messenger, messenger_address, id_generator, randomizer, node_addresses,
                               reply_queue, placements)

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, Reply):
            self._processor.process(ActorReplyAskCommand(
                address=sender, message=message.message, ref_id=message.ref_id,
            ))
        else:
            super(ActorSystemBase, self).handle_message(sender, receiver, message)

    def handle_processor_command(self, command: Command):
        if isinstance(command, MessageHandlingCommand) and command.receiver == self._root_address:
            self._root.receive(command.sender, command.message)
        elif isinstance(command, SystemSpawnActorCommand):
            self._node_spawn_process_for_user(command)
        elif isinstance(command, SystemAskCommand):
            self._system_ask(command)
        elif isinstance(command, ActorReplyAskCommand):
            self._actor_reply_ask(command)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def _node_spawn_process_for_user(self, command: SystemSpawnActorCommand):
        msg = NodeSpawnProcessMessage(
            address=self._address.child(command.key),
            type_=command.type_,
            ref_id=self._id_generator.generate(),
            initial_message=command.initial_message,
        )
        node = self._root.choose_placement_node(command.type_)
        self._messenger.send(self._address, node, msg)

    def spawn(self, key: str, actor_type: ProcessFactory, *, initial_message: Optional[Message] = None) -> Address:
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type, initial_message=initial_message))
        reply: SystemSpawnActorCompletedReply = self._reply_queue.get()
        return reply.address

    def tell(self, address: Address, message: Message):
        self._messenger.send(self._root_address, address, message)

    def ask(self, address: Address, message: Message) -> Message:
        ref_id = self._id_generator.generate()
        self._processor.process(SystemAskCommand(address=address, message=message, ref_id=ref_id))

        while True:
            reply: Reply = self._reply_queue.get()
            if reply.ref_id == ref_id:
                break
        return reply.message

    def _system_ask(self, command: SystemAskCommand):
        self._messenger.send(self._address, command.address, Ask(message=command.message, ref_id=command.ref_id))

    def _actor_reply_ask(self, command: ActorReplyAskCommand):
        self._reply_queue.put(ActorAskReply(address=command.address, message=command.message, ref_id=command.ref_id))

    def force_stop(self):
        for processor in self._processors:
            processor.stop()
