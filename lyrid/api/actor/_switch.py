from dataclasses import dataclass
from typing import Type, Callable, Any, List, Optional, TYPE_CHECKING

from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class Matching:
    type_: Optional[Type] = None

    def matches(self, _: Address, message: Message) -> bool:
        if self.type_ is not None:
            return isinstance(message, self.type_)
        return False


@dataclass
class HandleRule:
    matching: Matching
    execute: Callable[[Actor, Address, Message], Any]


class Switch:
    def __init__(self):
        self._rules: List[HandleRule] = []
        self.on_receive = OnReceive(self)

    def __get__(self, instance: Actor, owner=None):
        self._actor = instance
        return self

    # noinspection PyShadowingBuiltins
    def message(self, *, type: Type):
        return MessageMatcherDecorator(self, type_=type)

    def add_rule(self, rule: HandleRule):
        self._rules.append(rule)

    def __call__(self, actor: Actor, sender: Address, message: Message):
        for rule in self._rules:
            if rule.matching.matches(sender, message):
                rule.execute(actor, sender, message)
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


class MessageMatcherDecorator:
    def __init__(self, switch: Switch, type_: Type = None):
        self._switch_object = switch
        self._type = type_

    def __call__(self, f: Callable[[Actor, Address, Message], Any]):
        self._switch_object.add_rule(HandleRule(matching=Matching(type_=self._type), execute=f))
        return f
