import inspect
from typing import Type, List, Optional, TypeVar, Dict, Callable

from lyrid.api.actor.switch.handle_rule import HandlePolicy, HandleRule
from lyrid.api.actor.switch.property_injection import POLICY_PROPERTY, AFTER_RECEIVE_PROPERTY
from lyrid.base.actor import Actor
from lyrid.core.messaging import Message, Address


class OnReceiveDescriptor:
    def __init__(self, rules: List[HandleRule], after_receive: Optional[Callable]):
        self._rules = rules
        self._after_receive = after_receive
        self._method_map: Dict[int, OnReceiveMethod] = {}

    def __get__(self, instance, owner):
        id_ = id(instance)
        if id_ not in self._method_map:
            self._method_map[id_] = OnReceiveMethod(instance, self._rules, self._after_receive)
        method = self._method_map.get(id_, None)
        return method


class OnReceiveMethod:
    def __init__(self, actor: Actor, rules: List[HandleRule], after_receive: Optional[Callable]):
        self._actor = actor
        self._rules = rules
        self._after_receive = after_receive

    def __call__(self, sender: Address, message: Message):
        matched_rule = next((rule for rule in self._rules if rule.match(sender, message)), None)
        if matched_rule is None:
            return

        matched_rule.execute(self._actor, sender, message)
        if self._after_receive:
            self._after_receive(self._actor)


A = TypeVar("A", bound=Actor)


def use_switch(actor: Type[A]) -> Type[A]:
    rules: List[HandleRule] = []
    after_receive: Optional[Callable] = None

    for cls in inspect.getmro(actor):
        if not issubclass(cls, Actor) and cls is not Actor:
            continue
        for method in cls.__dict__.values():
            policy: Optional[HandlePolicy] = getattr(method, POLICY_PROPERTY, None)
            if policy is not None:
                rules.append(policy.create_handle_rule_with_function(method))

            if after_receive is None and getattr(method, AFTER_RECEIVE_PROPERTY, False):
                after_receive = method

    setattr(actor, "on_receive", OnReceiveDescriptor(rules, after_receive))
    return actor
