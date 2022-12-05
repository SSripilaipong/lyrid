from abc import abstractmethod
from typing import Protocol, Callable, Tuple, SupportsFloat


class BackgroundTaskExecutor(Protocol):

    @abstractmethod
    def execute(self, task: Callable, *, args: Tuple = ()):
        pass

    @abstractmethod
    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        pass
