from lyrid.base import ManagerBase
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messenger import IManager


def create_manager(scheduler: ITaskScheduler) -> IManager:
    return ManagerBase(scheduler=scheduler)
