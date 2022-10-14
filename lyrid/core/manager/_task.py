from dataclasses import dataclass
from typing import Deque

from lyrid.core.messaging import Address, Message


class Task:
    pass


class StopSchedulerTask(Task):
    pass


class ActorTargetedTask(Task):
    pass


@dataclass
class ActorMessageDeliveryTask(ActorTargetedTask):
    target: Address
    message: Message
    sender: Address


@dataclass
class ActorTargetedTaskGroup(ActorTargetedTask):
    target: Address
    actor_task_queue: Deque[ActorTargetedTask]
