import queue
from typing import List

from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler, ManagerSpawnActorMessage, ActorMessageSendingCommand
from lyrid.core.messaging import Address, Message, Ask, Reply
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import SystemSpawnActorCommand, SystemSpawnActorCompletedReply, ActorReplyAskCommand, \
    ActorAskReply
from ._root import RootActor
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
        self._reply_queue = reply_queue
        self._id_generator = id_generator
        self._processors = processors or []

        self._root = RootActor(root_address, messenger, messenger_address, id_generator, manager_addresses, reply_queue)

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, Reply):
            self._processor.process(ActorReplyAskCommand(
                address=sender, message=message.message, ref_id=message.ref_id,
            ))
        else:
            super(ActorSystemBase, self).handle_message(sender, receiver, message)

    def handle_processor_command(self, command: Command):
        if isinstance(command, ActorMessageSendingCommand) and command.receiver == self._root_address:
            self._root.receive(command.sender, command.message)
        elif isinstance(command, SystemSpawnActorCommand):
            self._manager_spawn_actor_for_user(command)
        elif isinstance(command, SystemAskCommand):
            self._system_ask(command)
        elif isinstance(command, ActorReplyAskCommand):
            self._actor_reply_ask(command)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def _manager_spawn_actor_for_user(self, command: SystemSpawnActorCommand):
        msg = ManagerSpawnActorMessage(
            address=self._address.child(command.key),
            type_=command.type_,
            ref_id=self._id_generator.generate(),
        )
        self._messenger.send(self._address, self._manager_addresses[0], msg)

    def spawn(self, key: str, actor_type: IActorFactory) -> Address:
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type))
        reply: SystemSpawnActorCompletedReply = self._reply_queue.get()
        return reply.address

    def ask(self, address: Address, message: Message) -> Message:
        ref_id = self._id_generator.generate()
        self._processor.process(SystemAskCommand(address=address, message=message, ref_id=ref_id))
        reply: Reply = self._reply_queue.get()
        return reply.message

    def _system_ask(self, command: SystemAskCommand):
        self._messenger.send(self._address, command.address, Ask(message=command.message, ref_id=command.ref_id))

    def _actor_reply_ask(self, command: ActorReplyAskCommand):
        self._reply_queue.put(ActorAskReply(address=command.address, message=command.message, ref_id=command.ref_id))

    def join(self):
        for processor in self._processors:
            processor.stop()
