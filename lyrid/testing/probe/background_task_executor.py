from dataclasses import dataclass
from typing import Callable, Tuple, SupportsFloat, List, Any

from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.messaging import Address


@dataclass
class ExecuteWithDelayEvent:
    task: Callable
    delay: SupportsFloat
    args: Tuple = ()


@dataclass
class ExecuteEvent:
    task_id: str
    task: Callable
    args: Tuple = ()


class BackgroundTaskExecutorProbe(BackgroundTaskExecutor):
    def __init__(self):
        self._execute_with_delay__subscribers: List[Callable[[ExecuteWithDelayEvent], Any]] = []
        self._execute__subscribers: List[Callable[[ExecuteEvent], Any]] = []

    def execute(self, task_id: str, address: Address, task: Callable, *, args: Tuple = ()):
        for callback in self._execute__subscribers:
            callback(ExecuteEvent(task_id, task, args))

    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        for callback in self._execute_with_delay__subscribers:
            callback(ExecuteWithDelayEvent(task, delay, args))

    def execute_with_delay__subscribe(self, callback: Callable[[ExecuteWithDelayEvent], Any]):
        self._execute_with_delay__subscribers.append(callback)

    def execute__subscribe(self, callback: Callable[[ExecuteEvent], Any]):
        self._execute__subscribers.append(callback)
