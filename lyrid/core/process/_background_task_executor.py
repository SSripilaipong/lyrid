from abc import abstractmethod
from typing import Protocol, Callable, Tuple, SupportsFloat

from lyrid.core.messaging import Address


class BackgroundTaskExecutor(Protocol):

    @abstractmethod
    def execute(self, address: Address, task: Callable, *, args: Tuple = ()):
        pass

    @abstractmethod
    def execute_with_delay(self, task: Callable, *, delay: SupportsFloat, args: Tuple = ()):
        pass
