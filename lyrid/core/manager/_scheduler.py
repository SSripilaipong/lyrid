from abc import abstractmethod
from typing import Protocol

from ._task import Task


class ITaskScheduler(Protocol):

    @abstractmethod
    def schedule(self, task: Task):
        pass
