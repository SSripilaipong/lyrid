# noinspection PyPep8Naming
from typing import Type, Optional

from lyrid.core.messaging import Message
from .decorator import PolicyDecorator, AfterReceiveDecorator
from .handle_policy.ask_message_type import AskMessageTypeHandlePolicy
from .handle_policy.background_task_exited import BackgroundTaskExitedHandlePolicy
from .handle_policy.child_spawned import ChildSpawnedHandlePolicy
from .handle_policy.child_stopped import ChildStoppedHandlePolicy
from .handle_policy.message_type import MessageTypeHandlePolicy


# noinspection PyPep8Naming,PyShadowingBuiltins
class switch:
    @classmethod
    def message(cls, *, type: Type[Message]):
        return PolicyDecorator(policy=MessageTypeHandlePolicy(type_=type))

    @classmethod
    def ask(cls, *, type: Type[Message]):
        return PolicyDecorator(policy=AskMessageTypeHandlePolicy(type_=type))

    @classmethod
    def child_stopped(cls, *, exception: Optional[Type[Exception]]):
        return PolicyDecorator(policy=ChildStoppedHandlePolicy(exception_type=exception))

    @classmethod
    def background_task_exited(cls, *, exception: Optional[Type[Exception]]):
        return PolicyDecorator(policy=BackgroundTaskExitedHandlePolicy(exception))

    @classmethod
    def child_spawned(cls):
        return PolicyDecorator(policy=ChildSpawnedHandlePolicy())

    @classmethod
    def after_receive(cls):
        return AfterReceiveDecorator()
