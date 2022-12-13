import inspect
from dataclasses import dataclass
from typing import Type, Callable, Dict, Any

from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class _RequiredParams:
    sender: bool
    message: bool


@dataclass
class MessageTypeHandlePolicy(HandlePolicy):
    type_: Type[Message]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        signature = inspect.signature(function)

        sender = signature.parameters.get("sender", None)
        message = signature.parameters.get("message", None)

        required_params = _RequiredParams(sender=sender is not None, message=message is not None)
        return MessageTypeHandleRule(type_=self.type_, function=function, required_params=required_params)


@dataclass
class MessageTypeHandleRule(HandleRule):
    type_: Type[Message]
    function: Callable
    required_params: _RequiredParams

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, self.type_)

    def execute(self, actor: Actor, sender: Address, message: Message):
        params: Dict[str, Any] = {}
        if self.required_params.message:
            params["message"] = message
        if self.required_params.sender:
            params["sender"] = sender
        self.function(actor, **params)
