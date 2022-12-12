from threading import Timer
from typing import Callable, Tuple, SupportsFloat

from lyrid.core.messaging import Address
from lyrid.core.process import BackgroundTaskExecutor
from ._threading_client import ThreadingClient


class ThreadBackgroundTaskExecutor(BackgroundTaskExecutor):
    def __init__(self, thread_client: ThreadingClient):
        self._thread_client = thread_client

    def execute(self, address: Address, task: Callable, *, args: Tuple = ()):
        self._thread_client.start_thread(task, args=args)

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        Timer(float(delay), task, args=args).start()
