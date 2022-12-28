from dataclasses import dataclass
from typing import Callable, Tuple, SupportsFloat, List, Any

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.messaging import Address


@dataclass
class ExecuteWithDelayEvent:
    task: Callable
    delay: SupportsFloat
    args: Tuple = ()


class BackgroundTaskExecutorProbe(BackgroundTaskExecutor):
    def __init__(self):
        self.execute_with_delay__tasks: List[Callable] = []
        self.execute_with_delay__delays: List[SupportsFloat] = []
        self.execute_with_delay__args: List[Tuple] = []

        self._execute_with_delay__subscribers: List[Callable[[ExecuteWithDelayEvent], Any]] = []

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        pass

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        self.execute_with_delay__tasks.append(task)
        self.execute_with_delay__delays.append(delay)
        self.execute_with_delay__args.append(args)

        for callback in self._execute_with_delay__subscribers:
            callback(ExecuteWithDelayEvent(task, delay, args))

    def execute_with_delay__subscribe(self, callback: Callable[[ExecuteWithDelayEvent], Any]):
        self._execute_with_delay__subscribers.append(callback)
