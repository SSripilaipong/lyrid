from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler
from lyrid.core.processor import IProcessor
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_manager(*, scheduler: ITaskScheduler = None, processor: IProcessor = None) -> ManagerBase:
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    return ManagerBase(scheduler=scheduler, processor=processor)
