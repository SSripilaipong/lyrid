from lyrid.base.background_task_executor import ThreadBackgroundTaskExecutor, ThreadingClient
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock
from tests.mock.thread_client import ThreadClientMock


def create_thread_background_task_executor(*, thread_client: ThreadingClient = None,
                                           messenger: IMessenger = None) -> ThreadBackgroundTaskExecutor:
    thread_client = thread_client or ThreadClientMock()
    messenger = messenger or MessengerMock()
    return ThreadBackgroundTaskExecutor(thread_client=thread_client, messenger=messenger)
