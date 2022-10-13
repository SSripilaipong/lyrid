from dataclasses import dataclass

from lyrid.core.messaging import Address, Message


class Task:
    pass


@dataclass
class ActorTask(Task):
    target: Address
    message: Message
    sender: Address
