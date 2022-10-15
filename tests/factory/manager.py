from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_manager(*, address: Address = None, scheduler: ITaskScheduler = None,
                   processor: IProcessor = None, messenger: IMessenger = None) -> ManagerBase:
    address = address or Address("$.me")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    return ManagerBase(address=address, scheduler=scheduler, processor=processor, messenger=messenger)
