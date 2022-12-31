# noinspection PyPep8Naming
from typing import Type, Callable, Optional

from lyrid.core.messaging import Message
from .handle_policy.ask_message_type import AskMessageTypeHandlePolicy
from .handle_policy.child_stopped import ChildStoppedHandlePolicy
from .handle_policy.message_type import MessageTypeHandlePolicy
from .handle_rule import HandlePolicy


# noinspection PyShadowingBuiltins,PyPep8Naming
class switch:
    @classmethod
    def message(cls, *, type: Type[Message]):
        return MethodDecorator(policy=MessageTypeHandlePolicy(type_=type))

    @classmethod
    def ask(cls, *, type: Type[Message]):
        return MethodDecorator(policy=AskMessageTypeHandlePolicy(type_=type))

    @classmethod
    def child_stopped(cls, *, exception: Optional[Type[Exception]]):
        return MethodDecorator(policy=ChildStoppedHandlePolicy(exception_type=exception))


class MethodDecorator:
    def __init__(self, policy: HandlePolicy):
        self._policy = policy

    def __call__(self, f: Callable) -> Callable:
        setattr(f, "_lyrid_switch_policy", self._policy)
        return f
