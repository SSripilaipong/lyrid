import inspect
from dataclasses import dataclass
from typing import Callable

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_annotated_as_type_error
from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message
from lyrid.core.system import SpawnChildCompleted


@dataclass
class _RequiredParams:
    address: bool = False


class ChildSpawnedHandlePolicy(HandlePolicy):
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
            else:
                raise invalid_argument_for_method_error(name, function_name)
        return ChildSpawnedHandleRule(function, required_params)


@dataclass
class ChildSpawnedHandleRule(HandleRule):
    function: Callable
    required_params: _RequiredParams

    def match(self, sender: Address, message: Message) -> bool:
        return isinstance(message, SpawnChildCompleted)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, SpawnChildCompleted)

        if self.required_params.address:
            self.function(actor, message.address)
        else:
            self.function(actor)
