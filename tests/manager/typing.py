from typing import Protocol

from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, IManager
from lyrid.core.processor import IProcessor


class ManagerFactory(Protocol):
    def __call__(self, *, address: Address = None, processor: IProcessor = None,
                 scheduler: ITaskScheduler = None, messenger: IMessenger = None,
                 supervisor_address: Address = None) -> IManager: ...
