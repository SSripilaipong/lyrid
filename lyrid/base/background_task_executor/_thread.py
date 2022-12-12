from threading import Timer
from typing import Callable, Tuple, SupportsFloat

from lyrid.core.background_task import BackgroundTaskExecutor, BackgroundTaskExited
from lyrid.core.messaging import Address
from ._threading_client import ThreadingClient
from ...core.messenger import IMessenger


class ThreadBackgroundTaskExecutor(BackgroundTaskExecutor):
    def __init__(self, thread_client: ThreadingClient, messenger: IMessenger):
        self._thread_client = thread_client
        self._messenger = messenger

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        self._thread_client.start_thread(self._background_task_wrapper(task, task_id, address), args=args)

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        Timer(float(delay), task, args=args).start()

    def _background_task_wrapper(self, task: Callable, task_id: str, address: Address):
        def wrapper(*args):
            try:
                return_value = task(*args)
                msg = BackgroundTaskExited(task_id, return_value=return_value)
            except Exception as e:
                msg = BackgroundTaskExited(task_id, exception=e)
            self._messenger.send(address, address, msg)

        return wrapper
