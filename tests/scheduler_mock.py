from lyrid.core.manager import Task


class SchedulerMock:

    def __init__(self):
        self.schedule__task = None

    def schedule(self, task: Task):
        self.schedule__task = task
