import inspect
from typing import Callable

from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error
from lyrid.api.actor.switch.handle_rule import HandlePolicy
from lyrid.api.actor.switch.property_injection import AFTER_RECEIVE_PROPERTY, POLICY_PROPERTY


class PolicyDecorator:
    def __init__(self, policy: HandlePolicy):
        self._policy = policy

    def __call__(self, f: Callable) -> Callable:
        setattr(f, POLICY_PROPERTY, self._policy)
        return f


class AfterReceiveDecorator:
    def __call__(self, f: Callable) -> Callable:
        signature = inspect.signature(f)
        for name in signature.parameters.keys():
            if name == "self":
                continue
            raise invalid_argument_for_method_error(name, f.__name__)
        setattr(f, AFTER_RECEIVE_PROPERTY, True)
        return f
