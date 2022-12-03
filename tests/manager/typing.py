from typing import Protocol

from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, IManager


class ManagerFactory(Protocol):
    def __call__(self, *, address: Address = None, processor: CommandProcessingLoop = None,
                 scheduler: ITaskScheduler = None, messenger: IMessenger = None,
                 supervisor_address: Address = None) -> IManager: ...
