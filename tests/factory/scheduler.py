from lyrid.base import ThreadedTaskScheduler
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock


def create_scheduler(messenger: IMessenger = None) -> ThreadedTaskScheduler:
    messenger = messenger or MessengerMock()
    return ThreadedTaskScheduler(messenger=messenger)
