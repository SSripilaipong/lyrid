import inspect
from dataclasses import dataclass
from typing import Callable, Optional, Type, Dict, Any

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_annotated_as_type_error
from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.process import ChildStopped


@dataclass
class _RequiredParams:
    address: bool = False
    exception: bool = False


@dataclass
class ChildStoppedHandlePolicy(HandlePolicy):
    exception_type: Optional[Type[Exception]]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        function_name = function.__name__
        signature = inspect.signature(function)

        required_params = _RequiredParams()
        for name, param in signature.parameters.items():
            if name == "self":
                continue
            elif name == "address":
                if param.annotation is not Address:
                    raise argument_in_method_must_be_annotated_as_type_error(name, function_name, Address.__name__)
                required_params.address = True
            elif name == "exception":
                if self.exception_type is None:
                    raise invalid_argument_for_method_error(name, function_name)
                if param.annotation is not self.exception_type:
                    raise argument_in_method_must_be_annotated_as_type_error(
                        name, function_name, self.exception_type.__name__,
                    )
                required_params.exception = True
            else:
                raise invalid_argument_for_method_error(name, function_name)
        return ChildStoppedHandleRule(self.exception_type, function, required_params)


@dataclass
class ChildStoppedHandleRule(HandleRule):
    exception_type: Optional[Type[Exception]]
    function: Callable
    required_params: _RequiredParams

    def match(self, sender: Address, message: Message) -> bool:
        if not isinstance(message, ChildStopped):
            return False
        if self.exception_type is None:
            return message.exception is None
        return isinstance(message.exception, self.exception_type)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, ChildStopped)

        params: Dict[str, Any] = {}
        if self.required_params.address:
            params["address"] = sender
        if self.required_params.exception:
            params["exception"] = message.exception
        self.function(actor, **params)
