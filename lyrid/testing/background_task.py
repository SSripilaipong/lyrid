from dataclasses import dataclass
from typing import Callable, Tuple


@dataclass
class BackgroundTask:
    task_id: str
    task: Callable
    args: Tuple = ()
