from threading import Thread
from typing import Callable, Tuple

from lyrid.core.actor import BackgroundTaskExecutor


class ThreadBackgroundTaskExecutor(BackgroundTaskExecutor):
    def execute(self, task: Callable, *, args: Tuple = ()):
        Thread(target=task, args=args).start()
