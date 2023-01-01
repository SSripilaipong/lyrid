import inspect
from dataclasses import dataclass
from typing import Callable, Optional, Type, Dict, Any

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error, \
    argument_in_method_must_be_annotated_as_type_error
from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.background_task import BackgroundTaskExited
from lyrid.core.messaging import Address, Message


@dataclass
class _RequiredParams:
    task_id: bool = False
    result: bool = False
    exception: bool = False


@dataclass
class BackgroundTaskExitedHandlePolicy(HandlePolicy):
    exception_type: Optional[Type[Exception]]

    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        function_name = function.__name__
        signature = inspect.signature(function)

        required_params = _RequiredParams()
        for name, param in signature.parameters.items():
            if name == "self":
                continue
            elif name == "task_id":
                if param.annotation is not str:
                    raise argument_in_method_must_be_annotated_as_type_error(name, function_name, str.__name__)
                required_params.task_id = True
            elif name == "result":
                if self.exception_type is not None:
                    raise invalid_argument_for_method_error(name, function_name)
                required_params.result = True
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

        return BackgroundTaskExitedHandleRule(self.exception_type, function, required_params)


@dataclass
class BackgroundTaskExitedHandleRule(HandleRule):
    exception_type: Optional[Type[Exception]]
    function: Callable
    required_params: _RequiredParams

    def match(self, sender: Address, message: Message) -> bool:
        if not isinstance(message, BackgroundTaskExited):
            return False

        if self.exception_type is None:
            return message.exception is None
        return isinstance(message.exception, self.exception_type)

    def execute(self, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, BackgroundTaskExited)

        params: Dict[str, Any] = {}
        if self.required_params.task_id:
            params["task_id"] = message.task_id
        if self.required_params.result:
            params["result"] = message.return_value
        if self.required_params.exception:
            params["exception"] = message.exception

        return self.function(actor, **params)
