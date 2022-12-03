from lyrid.base import ProcessManagingNode
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.node import TaskScheduler
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_process_managing_node(*, address: Address = None, scheduler: TaskScheduler = None,
                                 processor: CommandProcessingLoop = None,
                                 messenger: IMessenger = None) -> ProcessManagingNode:
    address = address or Address("$.me")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    return ProcessManagingNode(address=address, scheduler=scheduler, processor=processor, messenger=messenger)
