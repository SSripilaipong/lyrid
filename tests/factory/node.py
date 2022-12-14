from lyrid.base import ProcessManagingNode
from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.common import IdGenerator
from lyrid.core.messaging import Address
from lyrid.core.messenger import Messenger
from lyrid.core.node import TaskScheduler
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_process_managing_node(*, address: Address = None, scheduler: TaskScheduler = None,
                                 processor: CommandProcessingLoop = None,
                                 messenger: Messenger = None,
                                 background_task_executor: BackgroundTaskExecutor = None,
                                 id_generator: IdGenerator = None) -> ProcessManagingNode:
    address = address or Address("$.me")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    background_task_executor = background_task_executor or BackgroundTaskExecutorMock()
    id_generator = id_generator or IdGeneratorMock()
    return ProcessManagingNode(address=address, scheduler=scheduler, processor=processor, messenger=messenger,
                               background_task_executor=background_task_executor, id_generator=id_generator)
