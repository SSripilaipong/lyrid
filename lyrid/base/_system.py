import queue
from typing import List

from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler, ManagerSpawnActorMessage, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, MessengerRegisterAddressMessage
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import SystemSpawnActorCommand, AcknowledgeManagerSpawnActorCompletedCommand, \
    AcknowledgeMessengerRegisterAddressCompletedCommand, SystemSpawnActorCompletedReply
from ..core.actor import IActorFactory


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address], address: Address, messenger_address: Address,
                 reply_queue: queue.Queue):
        super().__init__(address=address, scheduler=scheduler, processor=processor, messenger=messenger)

        self._messenger = messenger
        self._manager_addresses = manager_addresses
        self._messenger_address = messenger_address
        self._reply_queue = reply_queue

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, ManagerSpawnActorCompletedMessage):
            self._processor.process(AcknowledgeManagerSpawnActorCompletedCommand(
                actor_address=message.actor_address, manager_address=message.manager_address,
            ))
        else:
            super(ActorSystemBase, self).handle_message(sender, receiver, message)

    def handle_processor_command(self, command: Command):
        if isinstance(command, SystemSpawnActorCommand):
            self._manager_spawn_actor(command)
        elif isinstance(command, AcknowledgeManagerSpawnActorCompletedCommand):
            self._messenger_register_address(command)
        elif isinstance(command, AcknowledgeMessengerRegisterAddressCompletedCommand):
            self._reply_system_spawn_completed(command)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def _messenger_register_address(self, command: AcknowledgeManagerSpawnActorCompletedCommand):
        msg = MessengerRegisterAddressMessage(address=command.actor_address, manager_address=command.manager_address)
        self._messenger.send(self._address, self._messenger_address, msg)

    def _manager_spawn_actor(self, command: SystemSpawnActorCommand):
        msg = ManagerSpawnActorMessage(address=self._address.child(command.key), type_=command.type_)
        self._messenger.send(self._address, self._manager_addresses[0], msg)

    def spawn(self, key: str, actor_type: IActorFactory):
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type))

    def _reply_system_spawn_completed(self, command: AcknowledgeMessengerRegisterAddressCompletedCommand):
        self._reply_queue.put(SystemSpawnActorCompletedReply(address=command.actor_address))
