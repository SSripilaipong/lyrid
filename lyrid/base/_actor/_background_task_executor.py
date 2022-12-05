from threading import Thread, Timer
from typing import Callable, Tuple, SupportsFloat

from lyrid.core.actor import BackgroundTaskExecutor


class ThreadBackgroundTaskExecutor(BackgroundTaskExecutor):
    def execute(self, task: Callable, *, args: Tuple = ()):
        Thread(target=task, args=args).start()

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        Timer(float(delay), task, args=args).start()
