from dataclasses import dataclass
from typing import Optional, SupportsFloat, List

from lyrid.core.messaging import Address, Message
from .mock import MessengerForTesting, BackgroundTaskExecutorForTesting


@dataclass
class CapturedMessage:
    receiver: Address
    message: Message
    delay: Optional[SupportsFloat] = None


class Captor:
    def __init__(self, messenger: MessengerForTesting, bg_task_executor: BackgroundTaskExecutorForTesting):
        self._messenger = messenger
        self._bg_task_executor = bg_task_executor

    def get_messages(self) -> List[CapturedMessage]:
        executor = self._bg_task_executor
        if executor.execute_with_delay__tasks:
            delayed_tasks = zip(
                executor.execute_with_delay__tasks, executor.execute_with_delay__delays,
                executor.execute_with_delay__args,
            )
            return [
                CapturedMessage(receiver, message, delay=delay)
                for task, delay, (_, receiver, message) in filter(lambda t: t[0] == self._messenger.send, delayed_tasks)
            ]

        receivers = self._messenger.send__receivers
        messages = self._messenger.send__messages

        return [CapturedMessage(receiver, message, delay=None) for receiver, message in zip(receivers, messages)]
