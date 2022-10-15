from typing import List

from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler, ManagerSpawnActorMessage, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import SystemSpawnActorCommand, AcknowledgeManagerSpawnActorCompletedCommand
from ..core.actor import IActorFactory


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address], address: Address = None):
        address = address or Address("$")
        super().__init__(address=address, scheduler=scheduler, processor=processor, messenger=messenger)

        self._messenger = messenger
        self._manager_addresses = manager_addresses

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, ManagerSpawnActorCompletedMessage):
            self._processor.process(AcknowledgeManagerSpawnActorCompletedCommand(
                actor_address=message.actor_address, manager_address=message.manager_address,
            ))
        else:
            super(ActorSystemBase, self).handle_message(sender, receiver, message)

    def handle_processor_command(self, command: Command):
        if isinstance(command, SystemSpawnActorCommand):
            cmd = ManagerSpawnActorMessage(address=self._address.child(command.key), type_=command.type_)
            self._messenger.send(self._address, self._manager_addresses[0], cmd)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def spawn(self, key: str, actor_type: IActorFactory):
        self._processor.process(SystemSpawnActorCommand(key=key, type_=actor_type))
