from typing import Callable, Tuple, Optional

from lyrid.core.actor import BackgroundTaskExecutor


class BackgroundTaskExecutorMock(BackgroundTaskExecutor):
    def __init__(self):
        self.execute__task: Optional[Callable] = None
        self.execute__args: Optional[Tuple] = None

    def execute(self, task: Callable, *, args: Tuple = ()):
        self.execute__task = task
        self.execute__args = args
