import threading
from collections import deque
from queue import Queue
from typing import Dict, Optional

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.node import (
    Task, ProcessMessageDeliveryTask, StopSchedulerTask, ProcessTargetedTaskGroup, ProcessTargetedTask, TaskScheduler,
)
from lyrid.core.process import Process, ProcessStoppedSignal


class ThreadedTaskScheduler(TaskScheduler):
    def __init__(self, messenger: IMessenger):
        self._messenger = messenger

        self._task_queue: Queue[Task] = Queue()
        self._process_tasks: Dict[Address, ProcessTargetedTaskGroup] = dict()
        self._processes: Dict[Address, Process] = dict()

        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def schedule(self, task: ProcessTargetedTask):
        if isinstance(task, ProcessMessageDeliveryTask):
            with self._lock:
                if task.target not in self._processes:
                    return

            self._add_process_targeted_task_to_queue(task)
        else:
            raise NotImplementedError()

    def register_process(self, address: Address, process: Process, *, initial_message: Optional[Message] = None):
        with self._lock:
            self._processes[address] = process

        if initial_message is not None:
            self.schedule(ProcessMessageDeliveryTask(address, initial_message, address.supervisor()))

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

            if isinstance(task, ProcessTargetedTaskGroup):
                self._handle_process_targeted_task(task)
            elif isinstance(task, StopSchedulerTask):
                break
            else:
                raise NotImplementedError()

    def _add_process_targeted_task_to_queue(self, task):
        with self._lock:
            tasks_in_queue = self._process_tasks.get(
                task.target,
                ProcessTargetedTaskGroup(target=task.target, process_task_queue=deque()),
            )
            if len(tasks_in_queue.process_task_queue) == 0:
                self._task_queue.put(tasks_in_queue)
            tasks_in_queue.process_task_queue.append(task)

    def _handle_process_targeted_task(self, task):
        if len(task.process_task_queue) == 0:
            return
        with self._lock:
            process = self._processes.get(task.target)

        if process is None:
            return

        process_task = task.process_task_queue.popleft()
        if isinstance(process_task, ProcessMessageDeliveryTask):
            try:
                process.receive(process_task.sender, process_task.message)
            except ProcessStoppedSignal:
                self._handle_stopped_process(task.target)
        else:
            raise NotImplementedError()

        if len(task.process_task_queue) > 0:
            self._task_queue.put(task)

    def _handle_stopped_process(self, address: Address):
        with self._lock:
            del self._processes[address]
