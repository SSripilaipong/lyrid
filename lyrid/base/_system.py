from typing import List

from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler, ManagerSpawnActorMessage, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, MessengerRegisterAddressMessage
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import SystemSpawnActorCommand, AcknowledgeManagerSpawnActorCompletedCommand
from ..core.actor import IActorFactory


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address], address: Address, messenger_address: Address):
        super().__init__(address=address, scheduler=scheduler, processor=processor, messenger=messenger)

        self._messenger = messenger
        self._manager_addresses = manager_addresses
        self._messenger_address = messenger_address

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
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def _messenger_register_address(self, command):
        msg = MessengerRegisterAddressMessage(address=command.actor_address, manager=command.manager_address)
        self._messenger.send(self._address, self._messenger_address, msg)

    def _manager_spawn_actor(self, command):
        msg = ManagerSpawnActorMessage(address=self._address.child(command.key), type_=command.type_)
        self._messenger.send(self._address, self._manager_addresses[0], msg)

    def spawn(self, key: str, actor_type: IActorFactory):
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type))
