from dataclasses import dataclass
from typing import Callable, Optional, Type

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.background_task import BackgroundTaskExited
from lyrid.core.messaging import Address, Message


@dataclass
class BackgroundTaskExitedHandlePolicy(HandlePolicy):
    exception: Optional[Type[Exception]]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return BackgroundTaskExitedHandleRule(self.exception, function)


@dataclass
class BackgroundTaskExitedHandleRule(HandleRule):
    exception_type: Optional[Type[Exception]]
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        if not isinstance(message, BackgroundTaskExited):
            return False

        if self.exception_type is None:
            return message.exception is None
        return True

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, BackgroundTaskExited)

        if self.exception_type is None:
            return self.function(actor, message.task_id, message.return_value)
        return self.function(actor, message.task_id, message.exception)
