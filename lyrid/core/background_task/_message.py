from dataclasses import dataclass

from lyrid.core.messaging import Message


@dataclass
class BackgroundTaskExited(Message):
    task_id: str
