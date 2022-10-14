from lyrid.core.actor import IActor
from lyrid.core.manager import ActorTargetedTask
from lyrid.core.messaging import Address


class SchedulerMock:

    def __init__(self):
        self.stop__is_called = False
        self.start__is_called = False
        self.schedule__task = None

    def schedule(self, task: ActorTargetedTask):
        self.schedule__task = task

    def register_actor(self, address: Address, actor: IActor):
        pass

    def stop(self):
        self.stop__is_called = True

    def start(self):
        self.start__is_called = True
