from typing import Optional

from lyrid import Message
from lyrid.core.messaging import Address
from lyrid.core.node import ProcessTargetedTask, TaskScheduler
from lyrid.core.process import Process


class SchedulerMock(TaskScheduler):

    def __init__(self, *, force_stop_actor__raise: Exception = None):
        self._force_stop_actor__raise = force_stop_actor__raise

        self.register_process__process: Optional[Process] = None
        self.register_process__address: Optional[Address] = None
        self.register_process__initial_message: Optional[Message] = None
        self.stop__is_called = False
        self.start__is_called = False
        self.schedule__task: Optional[ProcessTargetedTask] = None

    def schedule(self, task: ProcessTargetedTask):
        self.schedule__task = task

    def register_process(self, address: Address, process: Process, *, initial_message: Optional[Message] = None):
        self.register_process__address = address
        self.register_process__process = process
        self.register_process__initial_message = initial_message

    def stop(self):
        self.stop__is_called = True

    def start(self):
        self.start__is_called = True
