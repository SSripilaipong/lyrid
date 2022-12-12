from threading import Thread, Timer
from typing import Callable, Tuple, SupportsFloat

from lyrid.core.messaging import Address
from lyrid.core.process import BackgroundTaskExecutor


class ThreadBackgroundTaskExecutor(BackgroundTaskExecutor):
    def execute(self, address: Address, task: Callable, *, args: Tuple = ()):
        Thread(target=task, args=args).start()

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        Timer(float(delay), task, args=args).start()
