from dataclasses import dataclass
from typing import Type, Callable

from lyrid.api.actor.switch.handle_policy import HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class MessageTypeHandlePolicy(HandlePolicy):
    type_: Type

    def matches(self, sender: Address, message: Message) -> bool:
        if self.type_ is not None:
            return isinstance(message, self.type_)
        return False

    def decorate(self, f: Callable) -> Callable:
        return f

    def execute(self, f: Callable, actor: Actor, sender: Address, message: Message):
        f(actor, sender, message)
