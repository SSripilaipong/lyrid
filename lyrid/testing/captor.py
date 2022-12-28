from dataclasses import dataclass
from typing import Optional, SupportsFloat, List

from lyrid.core.messaging import Address, Message, LyridMessage
from .probe import MessengerProbe, BackgroundTaskExecutorProbe
from .probe.background_task_executor import ExecuteWithDelayEvent
from .probe.messenger import SendEvent


@dataclass(frozen=True)
class CapturedMessage:
    receiver: Address
    message: Message
    delay: Optional[SupportsFloat] = None


class Captor:
    def __init__(self, messenger: MessengerProbe, bg_task_executor: BackgroundTaskExecutorProbe):
        self._messenger = messenger
        self._messages: List[CapturedMessage] = []

        self._messenger.send__subscribe(self.__messenger__send)
        bg_task_executor.execute_with_delay__subscribe(self.__background_task_executor__execute_with_delay)

    def get_messages(self) -> List[CapturedMessage]:
        return list(self._messages)

    def clear_messages(self):
        self._messages = []

    def __messenger__send(self, event: SendEvent):
        if isinstance(event.message, LyridMessage):
            return
        self._messages.append(CapturedMessage(event.receiver, event.message))

    def __background_task_executor__execute_with_delay(self, event: ExecuteWithDelayEvent):
        if event.task != self._messenger.send:
            return

        _, receiver, message = event.args
        self._messages.append(CapturedMessage(receiver, message, delay=event.delay))
