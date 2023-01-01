from dataclasses import dataclass
from typing import Callable

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.system import SpawnChildCompleted


class ChildSpawnedHandlePolicy(HandlePolicy):
    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return ChildSpawnedHandleRule(function)


@dataclass
class ChildSpawnedHandleRule(HandleRule):
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, SpawnChildCompleted)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, SpawnChildCompleted)

        self.function(actor, message.address)
