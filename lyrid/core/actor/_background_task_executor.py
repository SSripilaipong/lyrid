from abc import abstractmethod
from typing import Protocol, Callable, Tuple


class BackgroundTaskExecutor(Protocol):

    @abstractmethod
    def execute(self, task: Callable, *, args: Tuple = ()):
        pass
