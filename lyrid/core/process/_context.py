from dataclasses import dataclass

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.common import IdGenerator
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger


@dataclass
class ProcessContext:
    address: Address
    messenger: IMessenger
    background_task_executor: BackgroundTaskExecutor
    id_generator: IdGenerator
