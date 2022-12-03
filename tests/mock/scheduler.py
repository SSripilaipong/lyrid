from typing import Optional

from lyrid.core.manager import ActorTargetedTask, ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.process import Process


class SchedulerMock(ITaskScheduler):

    def __init__(self, *, force_stop_actor__raise: Exception = None):
        self._force_stop_actor__raise = force_stop_actor__raise

        self.register_process__process: Optional[Process] = None
        self.register_process__address: Optional[Address] = None
        self.stop__is_called = False
        self.start__is_called = False
        self.schedule__task: Optional[ActorTargetedTask] = None
        self.force_stop_actor__address: Optional[Address] = None

    def schedule(self, task: ActorTargetedTask):
        self.schedule__task = task

    def register_process(self, address: Address, process: Process):
        self.register_process__address = address
        self.register_process__process = process

    def force_stop_actor(self, address: Address):
        self.force_stop_actor__address = address

        if self._force_stop_actor__raise is not None:
            raise self._force_stop_actor__raise

    def stop(self):
        self.stop__is_called = True

    def start(self):
        self.start__is_called = True
