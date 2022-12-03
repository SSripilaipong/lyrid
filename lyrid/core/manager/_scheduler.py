from abc import abstractmethod
from typing import Protocol

from ._task import ActorTargetedTask
from ..messaging import Address
from ..process import Process


class ITaskScheduler(Protocol):

    @abstractmethod
    def schedule(self, task: ActorTargetedTask):
        pass

    @abstractmethod
    def register_process(self, address: Address, process: Process):
        pass

    @abstractmethod
    def force_stop_actor(self, address: Address):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self):
        pass
