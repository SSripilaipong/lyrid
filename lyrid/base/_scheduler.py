import threading
from collections import deque
from queue import Queue
from typing import Dict, Optional

from lyrid.core.manager import (
    Task, ActorMessageDeliveryTask, StopSchedulerTask, ActorTargetedTaskGroup, ActorTargetedTask, ITaskScheduler,
)
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.process import Process, ProcessStoppedSignal


class TaskSchedulerBase(ITaskScheduler):
    def __init__(self, messenger: IMessenger):
        self._messenger = messenger

        self._task_queue: Queue[Task] = Queue()
        self._actor_tasks: Dict[Address, ActorTargetedTaskGroup] = dict()
        self._processes: Dict[Address, Process] = dict()

        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def schedule(self, task: ActorTargetedTask):
        if isinstance(task, ActorMessageDeliveryTask):
            with self._lock:
                if task.target not in self._processes:
                    return

                tasks_in_queue = self._actor_tasks.get(
                    task.target,
                    ActorTargetedTaskGroup(target=task.target, actor_task_queue=deque()),
                )
                if len(tasks_in_queue.actor_task_queue) == 0:
                    self._task_queue.put(tasks_in_queue)

                tasks_in_queue.actor_task_queue.append(task)
        else:
            raise NotImplementedError()

    def register_process(self, address: Address, process: Process):
        with self._lock:
            self._processes[address] = process

    def force_stop_actor(self, address: Address):
        with self._lock:
            if address in self._processes:
                del self._processes[address]

    def stop(self, block: bool = True):
        self._task_queue.put(StopSchedulerTask())
        if block:
            assert self._thread is not None
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
            actor = self._processes.get(task.target)

        if actor is None:
            return

        actor_task = task.actor_task_queue.popleft()
        if isinstance(actor_task, ActorMessageDeliveryTask):
            try:
                actor.receive(actor_task.sender, actor_task.message)
            except ProcessStoppedSignal:
                self._handle_stopped_actor(task.target)
        else:
            raise NotImplementedError()

        if len(task.actor_task_queue) > 0:
            self._task_queue.put(task)

    def _handle_stopped_actor(self, address: Address):
        with self._lock:
            del self._processes[address]
