from typing import Type, List, Optional, TypeVar, Dict

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.base.actor import Actor
from lyrid.core.messaging import Message, Address


class OnReceiveDescriptor:
    def __init__(self, rules: List[HandleRule]):
        self._rules = rules
        self._method_map: Dict[int, OnReceiveMethod] = {}

    def __get__(self, instance, owner):
        id_ = id(instance)
        if id_ not in self._method_map:
            self._method_map[id_] = OnReceiveMethod(instance, self._rules)
        method = self._method_map.get(id_, None)
        return method


class OnReceiveMethod:
    def __init__(self, actor: Actor, rules: List[HandleRule]):
        self._actor = actor
        self._rules = rules

    def __call__(self, sender: Address, message: Message):
        for rule in self._rules:
            if rule.match(sender, message):
                rule.execute(self._actor, sender, message)
                break


A = TypeVar("A", bound=Actor)


def use_switch(actor: Type[A]) -> Type[A]:
    rules: List[HandleRule] = []
    for name, method in actor.__dict__.items():
        policy: Optional[HandlePolicy] = getattr(method, "_lyrid_switch_policy", None)
        if policy is None:
            continue
        rules.append(policy.create_handle_rule_with_function(method))

    setattr(actor, "on_receive", OnReceiveDescriptor(rules))
    return actor
