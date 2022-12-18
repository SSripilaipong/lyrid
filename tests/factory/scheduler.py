from lyrid.base import ThreadedTaskScheduler
from lyrid.core.messenger import Messenger
from tests.mock.messenger import MessengerMock


def create_scheduler(messenger: Messenger = None) -> ThreadedTaskScheduler:
    messenger = messenger or MessengerMock()
    return ThreadedTaskScheduler(messenger=messenger)
