from typing import Type, Optional

from lyrid.core.messaging import Message
from .decorator import PolicyDecorator, AfterReceiveDecorator
from .handle_policy.ask_message_type import AskMessageTypeHandlePolicy
from .handle_policy.background_task_exited import BackgroundTaskExitedHandlePolicy
from .handle_policy.child_spawned import ChildSpawnedHandlePolicy
from .handle_policy.child_stopped import ChildStoppedHandlePolicy
from .handle_policy.message_type import MessageTypeHandlePolicy


# noinspection PyShadowingBuiltins
def message(*, type: Type[Message]):
    return PolicyDecorator(policy=MessageTypeHandlePolicy(type_=type))


# noinspection PyShadowingBuiltins
def ask(*, type: Type[Message]):
    return PolicyDecorator(policy=AskMessageTypeHandlePolicy(type_=type))


def child_stopped(*, exception: Optional[Type[Exception]]):
    return PolicyDecorator(policy=ChildStoppedHandlePolicy(exception_type=exception))


def background_task_exited(*, exception: Optional[Type[Exception]]):
    return PolicyDecorator(policy=BackgroundTaskExitedHandlePolicy(exception))


def child_spawned():
    return PolicyDecorator(policy=ChildSpawnedHandlePolicy())


def after_receive():
    return AfterReceiveDecorator()
