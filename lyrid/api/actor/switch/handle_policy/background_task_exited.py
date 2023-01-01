from dataclasses import dataclass
from typing import Callable

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.background_task import BackgroundTaskExited
from lyrid.core.messaging import Address, Message


@dataclass
class BackgroundTaskExitedHandlePolicy(HandlePolicy):

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return BackgroundTaskExitedHandleRule(function)


@dataclass
class BackgroundTaskExitedHandleRule(HandleRule):
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        return True

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, BackgroundTaskExited)

        self.function(actor, message.task_id, message.return_value)
