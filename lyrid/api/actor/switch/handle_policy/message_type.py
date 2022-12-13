import inspect
from dataclasses import dataclass
from typing import Type, Callable

from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class MessageTypeHandlePolicy(HandlePolicy):
    type_: Type[Message]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        signature = inspect.signature(function)
        need_message = signature.parameters.get("message", None) is not None
        return MessageTypeHandleRule(type_=self.type_, function=function, need_message=need_message)


@dataclass
class MessageTypeHandleRule(HandleRule):
    type_: Type[Message]
    function: Callable
    need_message: bool

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, self.type_)

    def execute(self, actor: Actor, sender: Address, message: Message):
        if self.need_message:
            self.function(actor, sender, message)
        else:
            self.function(actor, sender)
