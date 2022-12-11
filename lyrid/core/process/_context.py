from dataclasses import dataclass

from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.process import BackgroundTaskExecutor


@dataclass
class ProcessContext:
    address: Address
    messenger: IMessenger
    background_task_executor: BackgroundTaskExecutor
