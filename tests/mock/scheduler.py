from lyrid.core.actor import IActor
from lyrid.core.manager import Task
from lyrid.core.messaging import Address


class SchedulerMock:

    def __init__(self):
        self.schedule__task = None

    def schedule(self, task: Task):
        self.schedule__task = task

    def register_actor(self, address: Address, actor: IActor):
        pass
