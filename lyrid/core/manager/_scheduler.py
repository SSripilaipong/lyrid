from abc import abstractmethod
from typing import Protocol

from ._task import ActorTargetedTask
from ..actor import IActor
from ..messaging import Address


class ITaskScheduler(Protocol):

    @abstractmethod
    def schedule(self, task: ActorTargetedTask):
        pass

    @abstractmethod
    def register_actor(self, address: Address, actor: IActor):
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
