from dataclasses import dataclass
from typing import Type, Callable, Any, List, TYPE_CHECKING

from lyrid.base import Actor
from lyrid.core.messaging import Address, Message
from .handle_policy import HandlePolicy
from .handle_policy.ask_message_type import AskMessageTypeHandlePolicy
from .handle_policy.message_type import MessageTypeHandlePolicy


@dataclass
class HandleRule:
    policy: HandlePolicy
    function: Callable[[Actor, Address, Message], Any]


class Switch:
    def __init__(self):
        self._rules: List[HandleRule] = []
        self.on_receive = OnReceive(self)

    def __get__(self, instance: Actor, owner=None):
        self._actor = instance
        return self

    # noinspection PyShadowingBuiltins
    def message(self, *, type: Type[Message]):
        return FunctionDecorator(self, policy=MessageTypeHandlePolicy(type_=type))

    # noinspection PyShadowingBuiltins
    def ask(self, *, type: Type[Message]):
        return FunctionDecorator(self, policy=AskMessageTypeHandlePolicy(type_=type))

    def add_rule(self, rule: HandleRule):
        self._rules.append(rule)

    def __call__(self, actor: Actor, sender: Address, message: Message):
        for rule in self._rules:
            if rule.policy.matches(sender, message):
                rule.policy.execute(rule.function, actor, sender, message)
                break


class OnReceive:
    def __init__(self, switch: Switch):
        self._switch = switch

    def __get__(self, instance, owner=None):
        self._actor = instance
        return self

    if TYPE_CHECKING:
        @staticmethod
        def __call__(actor: Actor, sender: Address, message: Message):
            pass
    else:
        def __call__(self, sender: Address, message: Message):
            self._switch(self._actor, sender, message)


class FunctionDecorator:
    def __init__(self, switch: Switch, policy: HandlePolicy):
        self._switch_object = switch
        self._policy = policy

    def __call__(self, f: Callable) -> Callable:
        f = self._policy.decorate(f)
        self._switch_object.add_rule(HandleRule(policy=self._policy, function=f))
        return f
