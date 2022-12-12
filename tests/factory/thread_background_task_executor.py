from lyrid.base.background_task_executor import ThreadBackgroundTaskExecutor, ThreadingClient
from tests.mock.thread_client import ThreadClientMock


def create_thread_background_task_executor(*, thread_client: ThreadingClient = None) -> ThreadBackgroundTaskExecutor:
    thread_client = thread_client or ThreadClientMock()
    return ThreadBackgroundTaskExecutor(thread_client)
