from lyrid.base import TaskSchedulerBase
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock


def create_scheduler(messenger: IMessenger = None) -> TaskSchedulerBase:
    messenger = messenger or MessengerMock()
    return TaskSchedulerBase(messenger=messenger)
