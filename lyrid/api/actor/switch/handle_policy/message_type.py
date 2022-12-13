from dataclasses import dataclass
from typing import Type, Callable

from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class MessageTypeHandlePolicy(HandlePolicy):
    type_: Type[Message]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        return MessageTypeHandleRule(type_=self.type_, function=function)


@dataclass
class MessageTypeHandleRule(HandleRule):
    type_: Type[Message]
    function: Callable

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, self.type_)

    def execute(self, actor: Actor, sender: Address, message: Message):
        self.function(actor, sender, message)
