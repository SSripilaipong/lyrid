from typing import Callable, Tuple, SupportsFloat, List

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.messaging import Address


class BackgroundTaskExecutorForTesting(BackgroundTaskExecutor):
    def __init__(self):
        self.execute_with_delay__tasks: List[Callable] = []
        self.execute_with_delay__delays: List[SupportsFloat] = []
        self.execute_with_delay__args: List[Tuple] = []

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        pass

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        self.execute_with_delay__tasks.append(task)
        self.execute_with_delay__delays.append(delay)
        self.execute_with_delay__args.append(args)
