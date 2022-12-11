from typing import Protocol

from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, Node
from lyrid.core.node import TaskScheduler
from lyrid.core.process import BackgroundTaskExecutor


class NodeFactory(Protocol):
    def __call__(self, *, address: Address = None, processor: CommandProcessingLoop = None,
                 scheduler: TaskScheduler = None, messenger: IMessenger = None,
                 supervisor_address: Address = None,
                 background_task_executor: BackgroundTaskExecutor = None) -> Node: ...
