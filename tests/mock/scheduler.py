from lyrid.core.actor import IActor
from lyrid.core.manager import ActorTargetedTask, ITaskScheduler
from lyrid.core.messaging import Address


class SchedulerMock(ITaskScheduler):

    def __init__(self):
        self.register_actor__actor = None
        self.register_actor__address = None
        self.stop__is_called = False
        self.start__is_called = False
        self.schedule__task = None
        self.force_stop_actor__address = None

    def schedule(self, task: ActorTargetedTask):
        self.schedule__task = task

    def register_actor(self, address: Address, actor: IActor):
        self.register_actor__address = address
        self.register_actor__actor = actor

    def force_stop_actor(self, address: Address):
        self.force_stop_actor__address = address

    def stop(self):
        self.stop__is_called = True

    def start(self):
        self.start__is_called = True
