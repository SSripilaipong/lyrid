from dataclasses import dataclass
from typing import Deque

from lyrid.core.messaging import Address, Message


class Task:
    pass


class StopSchedulerTask(Task):
    pass


class ProcessTargetedTask(Task):
    pass


@dataclass
class ProcessMessageDeliveryTask(ProcessTargetedTask):
    target: Address
    message: Message
    sender: Address


@dataclass
class ProcessTargetedTaskGroup(ProcessTargetedTask):
    target: Address
    process_task_queue: Deque[ProcessTargetedTask]
