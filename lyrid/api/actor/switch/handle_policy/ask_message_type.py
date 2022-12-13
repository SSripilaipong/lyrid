from dataclasses import dataclass
from typing import Type, Callable

from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.messaging import Ask


@dataclass
class AskMessageTypeHandlePolicy(HandlePolicy):
    type_: Type[Message]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return AskMessageTypeHandleRule(type_=self.type_, function=function)


@dataclass
class AskMessageTypeHandleRule(HandleRule):
    type_: Type[Message]
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, Ask) and isinstance(message.message, self.type_)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, Ask)
        self.function(actor, sender, message.message, message.ref_id)
