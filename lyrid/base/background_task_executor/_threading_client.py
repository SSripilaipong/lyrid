from abc import abstractmethod
from typing import Protocol, Callable, Tuple


class ThreadingClient(Protocol):

    @abstractmethod
    def start_thread(self, function: Callable, *, args: Tuple):
        pass

    @abstractmethod
    def start_timer_thread(self, interval: float, function: Callable, *, args: Tuple = None):
        pass
