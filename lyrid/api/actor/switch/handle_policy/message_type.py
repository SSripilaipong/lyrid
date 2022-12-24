import inspect
from dataclasses import dataclass
from typing import Type, Callable, Dict, Any

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_function_error
from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class _RequiredParams:
    sender: bool = False
    message: bool = False


@dataclass
class MessageTypeHandlePolicy(HandlePolicy):
    type_: Type[Message]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        function_name = function.__name__
        signature = inspect.signature(function)
        required_params = _RequiredParams()

        for name, param in signature.parameters.items():
            if name == "self":
                continue
            elif name == "sender":
                if not isinstance(param.annotation, type) or not issubclass(param.annotation, Address):
                    raise TypeError(f"'{name}' argument in method '{function_name}' "
                                    f"must be annotated with type 'Address'")
                required_params.sender = True

            elif name == "message":
                if param.annotation != self.type_:
                    raise TypeError(f"'{name}' argument in method '{function_name}' "
                                    f"must be annotated with type '{self.type_.__name__}'")
                required_params.message = True
            else:
                raise invalid_argument_for_function_error(name, function_name)

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
