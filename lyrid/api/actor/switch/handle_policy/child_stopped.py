from dataclasses import dataclass
from typing import Callable

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message


class ChildStoppedHandlePolicy(HandlePolicy):
    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return ChildStoppedHandleRule(function)


@dataclass
class ChildStoppedHandleRule(HandleRule):
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        return True

    def execute(self, actor: Actor, sender: Address, message: Message):
        self.function(actor, sender)
