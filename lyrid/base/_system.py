from typing import Type, List

from lyrid.base import ManagerBase
from lyrid.core.actor import IActor
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor
from lyrid.core.system import ManagerSpawnActorCommand


class ActorSystemBase(ManagerBase):
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger,
                 manager_addresses: List[Address]):
        super().__init__(scheduler=scheduler, processor=processor)

        self._messenger = messenger
        self._manager_addresses = manager_addresses
        self._address = Address("$")

    def spawn(self, key: str, actor_type: Type[IActor]):
        cmd = ManagerSpawnActorCommand(address=self._address.child(key), type_=actor_type)
        self._messenger.send(self._address, self._manager_addresses[0], cmd)
