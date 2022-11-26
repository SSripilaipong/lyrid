import queue
from typing import List, Dict

from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler, ManagerSpawnActorMessage, ActorMessageSendingCommand, \
    ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address, Message, Ask, Reply
from lyrid.core.messenger import IMessenger, MessengerRegisterAddressMessage, MessengerRegisterAddressCompletedMessage
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import SystemSpawnActorCommand, SystemSpawnActorCompletedReply, ActorReplyAskCommand, \
    ActorAskReply, SpawnChildCompletedMessage, SpawnChildMessage
from ._task import ActorSpawnChildTask, Task
from ...core.actor import IActorFactory
from ...core.common import IIdGenerator
from ...core.system import SystemAskCommand


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address], root_address: Address, address: Address, messenger_address: Address,
                 reply_queue: queue.Queue, id_generator: IIdGenerator, processors: List[IProcessor] = None):
        super().__init__(address=address, scheduler=scheduler, processor=processor, messenger=messenger)

        self._root_address = root_address
        self._messenger = messenger
        self._manager_addresses = manager_addresses
        self._messenger_address = messenger_address
        self._reply_queue = reply_queue
        self._id_generator = id_generator
        self._processors = processors or []

        self._tasks: Dict[str, Task] = {}

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if not self._handle_message_as_root_actor(sender, receiver, message):
            super(ActorSystemBase, self).handle_message(sender, receiver, message)

    def handle_processor_command(self, command: Command):
        if isinstance(command, ActorMessageSendingCommand):
            if isinstance(command.message, ManagerSpawnActorCompletedMessage):
                self._messenger_register_address(command)
            elif isinstance(command.message, SpawnChildMessage):
                self._actor_spawn_child_actor(command)
            elif isinstance(command.message, MessengerRegisterAddressCompletedMessage):
                self._complete_spawning_actor(command)
            else:
                super(ActorSystemBase, self).handle_processor_command(command)
        elif isinstance(command, SystemSpawnActorCommand):
            self._manager_spawn_actor_for_user(command)
        elif isinstance(command, SystemAskCommand):
            self._system_ask(command)
        elif isinstance(command, ActorReplyAskCommand):
            self._actor_reply_ask(command)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def _messenger_register_address(self, command: ActorMessageSendingCommand[ManagerSpawnActorCompletedMessage]):
        msg = MessengerRegisterAddressMessage(address=command.message.actor_address,
                                              manager_address=command.sender,
                                              ref_id=command.message.ref_id)
        self._messenger.send(self._address, self._messenger_address, msg)

    def _manager_spawn_actor_for_user(self, command: SystemSpawnActorCommand):
        msg = ManagerSpawnActorMessage(
            address=self._address.child(command.key),
            type_=command.type_,
            ref_id=self._id_generator.generate(),
        )
        self._messenger.send(self._address, self._manager_addresses[0], msg)

    def _actor_spawn_child_actor(self, command: ActorMessageSendingCommand[SpawnChildMessage]):
        requester, child_key = command.sender, command.message.key
        ref_id = self._id_generator.generate()
        self._tasks[ref_id] = ActorSpawnChildTask(requester=requester, child_key=child_key)

        msg = ManagerSpawnActorMessage(
            address=requester.child(child_key),
            type_=command.message.type_,
            ref_id=ref_id,
        )
        self._messenger.send(self._address, self._manager_addresses[0], msg)

    def spawn(self, key: str, actor_type: IActorFactory) -> Address:
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type))
        reply: SystemSpawnActorCompletedReply = self._reply_queue.get()
        return reply.address

    def _complete_spawning_actor(self, command: ActorMessageSendingCommand[MessengerRegisterAddressCompletedMessage]):
        task = self._tasks.get(command.message.ref_id, None)
        if isinstance(task, ActorSpawnChildTask):
            self._messenger.send(self._address, task.requester,
                                 SpawnChildCompletedMessage(key=task.child_key, address=command.message.address))
            del self._tasks[command.message.ref_id]
        else:
            self._reply_queue.put(SystemSpawnActorCompletedReply(address=command.message.address))

    def ask(self, address: Address, message: Message) -> Message:
        ref_id = self._id_generator.generate()
        self._processor.process(SystemAskCommand(address=address, message=message, ref_id=ref_id))
        reply: Reply = self._reply_queue.get()
        return reply.message

    def _system_ask(self, command: SystemAskCommand):
        self._messenger.send(self._address, command.address, Ask(message=command.message, ref_id=command.ref_id))

    def _actor_reply_ask(self, command: ActorReplyAskCommand):
        self._reply_queue.put(ActorAskReply(address=command.address, message=command.message, ref_id=command.ref_id))

    def _handle_message_as_root_actor(self, sender: Address, receiver: Address, message: Message):
        is_handled = True
        if receiver != self._root_address:
            is_handled = False
        elif isinstance(message, Reply):
            self._processor.process(ActorReplyAskCommand(
                address=sender, message=message.message, ref_id=message.ref_id,
            ))
        else:
            is_handled = False
        return is_handled

    def join(self):
        for processor in self._processors:
            processor.stop()
