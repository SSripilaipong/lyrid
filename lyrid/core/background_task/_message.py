from dataclasses import dataclass
from typing import Any

from lyrid.core.messaging import Message


@dataclass
class BackgroundTaskExited(Message):
    task_id: str
    return_value: Any = None
