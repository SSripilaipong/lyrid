import threading
from typing import Callable, Tuple

from lyrid.base.background_task_executor import ThreadingClient


class BuiltinThreadingClient(ThreadingClient):
    def start_thread(self, function: Callable, *, args: Tuple):
        threading.Thread(target=function, args=args).start()

    def start_timer_thread(self, interval: float, function: Callable, *, args: Tuple = None):
        threading.Timer(interval, function, args=args).start()
