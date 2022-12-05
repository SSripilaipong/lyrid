from typing import Callable, Tuple, Optional, SupportsFloat

from lyrid.core.actor import BackgroundTaskExecutor


class BackgroundTaskExecutorMock(BackgroundTaskExecutor):
    def __init__(self):
        self.execute__task: Optional[Callable] = None
        self.execute__args: Optional[Tuple] = None

        self.execute_with_delay__task: Optional[Callable] = None
        self.execute_with_delay__args: Optional[Tuple] = None

    def execute(self, task: Callable, *, args: Tuple = ()):
        self.execute__task = task
        self.execute__args = args

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        self.execute_with_delay__task = task
        self.execute_with_delay__args = args
