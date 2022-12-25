import inspect
from dataclasses import dataclass
from typing import Type, Callable, Dict, Any

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_included_as_type_error, argument_in_method_must_be_annotated_as_type_error
from lyrid.api.actor.switch.handle_rule import HandleRule, HandlePolicy
from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.messaging import Ask


@dataclass
class _RequiredParams:
    sender: bool = False
    ref_id: bool = False
    message: bool = False


@dataclass
class AskMessageTypeHandlePolicy(HandlePolicy):
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
                    raise argument_in_method_must_be_annotated_as_type_error(name, function_name, Address.__name__)
                required_params.sender = True
            elif name == "message":
                if not isinstance(param.annotation, type) or not issubclass(param.annotation, self.type_):
                    raise argument_in_method_must_be_annotated_as_type_error(name, function_name, self.type_.__name__)
                required_params.message = True
            elif name == "ref_id":
                if not isinstance(param.annotation, type) or not issubclass(param.annotation, str):
                    raise argument_in_method_must_be_annotated_as_type_error(name, function_name, "str")
                required_params.ref_id = True
            else:
                raise invalid_argument_for_method_error(name, function_name)

        if not required_params.sender:
            raise argument_in_method_must_be_included_as_type_error("sender", function_name, Address.__name__)
        if not required_params.ref_id:
            raise argument_in_method_must_be_included_as_type_error("ref_id", function_name, "str")

        return AskMessageTypeHandleRule(type_=self.type_, function=function, required_params=required_params)


@dataclass
class AskMessageTypeHandleRule(HandleRule):
    type_: Type[Message]
    function: Callable
    required_params: _RequiredParams

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, Ask) and isinstance(message.message, self.type_)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, Ask)

        params: Dict[str, Any] = {}
        if self.required_params.message:
            params["message"] = message.message
        if self.required_params.sender:
            params["sender"] = sender
        if self.required_params.ref_id:
            params["ref_id"] = message.ref_id
        self.function(actor, **params)
