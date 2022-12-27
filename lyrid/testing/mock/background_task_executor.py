from typing import Callable, Tuple, SupportsFloat

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.messaging import Address


class BackgroundTaskExecutorForTesting(BackgroundTaskExecutor):
    def __init__(self):
        pass

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        pass

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        pass
