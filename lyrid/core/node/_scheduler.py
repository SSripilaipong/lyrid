from abc import abstractmethod
from typing import Protocol, Optional

from ._task import ProcessTargetedTask
from ..messaging import Address, Message
from ..process import Process


class TaskScheduler(Protocol):

    @abstractmethod
    def schedule(self, task: ProcessTargetedTask):
        pass

    @abstractmethod
    def register_process(self, address: Address, process: Process, *, initial_message: Optional[Message] = None):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self):
        pass
