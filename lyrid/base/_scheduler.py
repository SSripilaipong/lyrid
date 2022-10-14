import threading
from collections import deque
from queue import Queue
from typing import Dict, Optional

from lyrid.core.actor import IActor
from lyrid.core.manager import (
    Task, ActorMessageDeliveryTask, StopSchedulerTask, ActorTargetedTaskGroup, ActorTargetedTask,
)
from lyrid.core.messaging import Address


class TaskSchedulerBase:
    def __init__(self):
        self._task_queue: Queue[Task] = Queue()
        self._actor_tasks: Dict[Address, ActorTargetedTaskGroup] = dict()
        self._actors: Dict[Address, IActor] = dict()

        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def schedule(self, task: ActorTargetedTask):
        if isinstance(task, ActorMessageDeliveryTask):
            with self._lock:
                if task.target not in self._actors:
                    raise NotImplementedError()

                tasks_in_queue = self._actor_tasks.get(task.target,
                                                       ActorTargetedTaskGroup(target=task.target,
                                                                              actor_task_queue=deque()))
                if len(tasks_in_queue.actor_task_queue) == 0:
                    self._task_queue.put(tasks_in_queue)

                tasks_in_queue.actor_task_queue.append(task)
        else:
            raise NotImplementedError()

    def register_actor(self, address: Address, actor: IActor):
        with self._lock:
            self._actors[address] = actor

    def stop(self):
        self._task_queue.put(StopSchedulerTask())
        self._thread.join()

    def start(self):
        self._thread = threading.Thread(target=self._scheduler_loop)
        self._thread.start()

    def _scheduler_loop(self):
        while True:
            task = self._task_queue.get()

            if isinstance(task, ActorTargetedTaskGroup):
                self._handle_actor_targeted_task(task)
            elif isinstance(task, StopSchedulerTask):
                break
            else:
                raise NotImplementedError()

    def _handle_actor_targeted_task(self, task):
        if len(task.actor_task_queue) == 0:
            return
        with self._lock:
            actor = self._actors[task.target]

        actor_task = task.actor_task_queue.popleft()
        if isinstance(actor_task, ActorMessageDeliveryTask):
            actor.receive(actor_task.sender, actor_task.message)
        else:
            raise NotImplementedError()

        if len(task.actor_task_queue) > 0:
            self._task_queue.put(task)
