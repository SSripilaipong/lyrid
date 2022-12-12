from typing import Callable, Tuple, Optional

from lyrid.base.background_task_executor import ThreadingClient


class ThreadClientMock(ThreadingClient):
    def __init__(self):
        self.start_thread__function: Optional[Callable] = None
        self.start_thread__args: Optional[Tuple] = None

    def start_thread(self, function: Callable, *, args: Tuple):
        self.start_thread__function = function
        self.start_thread__args = args

    def start_timer_thread(self, interval: float, function: Callable, *, args: Tuple = None):
        pass
