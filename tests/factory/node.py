from lyrid.base import ProcessManagingNode
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.node import TaskScheduler
from lyrid.core.process import BackgroundTaskExecutor
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_process_managing_node(*, address: Address = None, scheduler: TaskScheduler = None,
                                 processor: CommandProcessingLoop = None,
                                 messenger: IMessenger = None,
                                 background_task_executor: BackgroundTaskExecutor = None) -> ProcessManagingNode:
    address = address or Address("$.me")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    background_task_executor = background_task_executor or BackgroundTaskExecutorMock()
    return ProcessManagingNode(address=address, scheduler=scheduler, processor=processor, messenger=messenger,
                               background_task_executor=background_task_executor)
