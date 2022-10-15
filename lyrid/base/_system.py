from typing import Type, List

from lyrid.base import ManagerBase
from lyrid.core.actor import IActor
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor, Command
from lyrid.core.system import ManagerSpawnActorMessage, SpawnActorCommand


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address]):
        super().__init__(scheduler=scheduler, processor=processor)

        self._messenger = messenger
        self._manager_addresses = manager_addresses
        self._address = Address("$")

    def handle_processor_command(self, command: Command):
        if isinstance(command, SpawnActorCommand):
            cmd = ManagerSpawnActorMessage(address=self._address.child(command.key), type_=command.type_)
            self._messenger.send(self._address, self._manager_addresses[0], cmd)
        else:
            super(ActorSystemBase, self).handle_processor_command(command)

    def spawn(self, key: str, actor_type: Type[IActor]):
        self._processor.process(SpawnActorCommand(key=key, type_=actor_type))
