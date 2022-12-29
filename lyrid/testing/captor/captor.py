from typing import Optional, List

from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Address, Message, LyridMessage, Reply
from lyrid.core.system import SpawnChildMessage
from lyrid.testing.probe import MessengerProbe, BackgroundTaskExecutorProbe
from lyrid.testing.probe.background_task_executor import ExecuteWithDelayEvent, ExecuteEvent
from lyrid.testing.probe.messenger import SendEvent
from .data import CapturedMessage, CapturedSpawnedChild
from ..background_task import BackgroundTask


class Captor:
    def __init__(self, actor_address: Address, messenger: MessengerProbe,
                 bg_task_executor: BackgroundTaskExecutorProbe):
        self._actor_address = actor_address
        self._messenger = messenger
        self._messages: List[CapturedMessage] = []
        self._replies: List[Reply] = []
        self._spawned_children: List[CapturedSpawnedChild] = []
        self._background_tasks: List[BackgroundTask] = []

        self._messenger.send__subscribe(self.__messenger__send)
        bg_task_executor.execute_with_delay__subscribe(self.__background_task_executor__execute_with_delay)
        bg_task_executor.execute__subscribe(self.__background_task_executor__execute)

    def get_messages(self) -> List[CapturedMessage]:
        return list(self._messages)

    def clear_messages(self):
        self._messages = []

    def get_reply(self, ref_id: str) -> Optional[Message]:
        for reply in self._replies:
            if reply.ref_id == ref_id:
                return reply.message
        return None

    def clear_replies(self):
        self._replies = []

    def __messenger__send(self, event: SendEvent):
        if isinstance(event.message, Reply):
            if event.receiver != Address("$"):
                return
            self._replies.append(event.message)
        elif isinstance(event.message, SpawnChildMessage):
            assert isinstance(event.message.process, ActorProcess)
            self._spawned_children.append(CapturedSpawnedChild(
                event.message.process.actor,
                self._actor_address.child(event.message.key),
                initial_message=event.message.initial_message,
            ))
        elif isinstance(event.message, LyridMessage):
            return
        else:
            self._messages.append(CapturedMessage(event.receiver, event.message))

    def __background_task_executor__execute(self, event: ExecuteEvent):
        self._background_tasks.append(BackgroundTask(event.task_id, event.task, event.args))

    def __background_task_executor__execute_with_delay(self, event: ExecuteWithDelayEvent):
        if event.task != self._messenger.send:
            return

        _, receiver, message = event.args
        self._messages.append(CapturedMessage(receiver, message, delay=event.delay))

    def get_spawned_children(self, address: Address = None) -> List[CapturedSpawnedChild]:
        if address:
            return [child for child in self._spawned_children if child.address == address]
        return list(self._spawned_children)

    def clear_spawned_children(self):
        self._spawned_children = []

    def get_background_tasks(self) -> List[BackgroundTask]:
        return list(self._background_tasks)

    def clear_background_tasks(self):
        self._background_tasks = []
