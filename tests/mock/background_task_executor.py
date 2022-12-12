from typing import Callable, Tuple, Optional, SupportsFloat

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.messaging import Address


class BackgroundTaskExecutorMock(BackgroundTaskExecutor):
    def __init__(self):
        self.execute__task_id: Optional[str] = None
        self.execute__address: Optional[Address] = None
        self.execute__task: Optional[Callable] = None
        self.execute__args: Optional[Tuple] = None

        self.execute_with_delay__task: Optional[Callable] = None
        self.execute_with_delay__args: Optional[Tuple] = None
        self.execute_with_delay__delay: Optional[SupportsFloat] = None

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        self.execute__task_id = task_id
        self.execute__address = address
        self.execute__task = task
        self.execute__args = args

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        self.execute_with_delay__task = task
        self.execute_with_delay__args = args
        self.execute_with_delay__delay = delay
