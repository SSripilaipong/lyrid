from dataclasses import dataclass
from typing import Type, Callable

from lyrid.api.actor.switch.handle_policy import HandlePolicy
from lyrid.base import Actor
from lyrid.core.messaging import Address, Message, Ask


@dataclass
class AskMessageTypeHandlePolicy(HandlePolicy):
    type_: Type

    def matches(self, sender: Address, message: Message) -> bool:
        return isinstance(message, Ask) and isinstance(message.message, self.type_)

    def decorate(self, f: Callable) -> Callable:
        return f

    def execute(self, f: Callable, actor: Actor, sender: Address, message: Message):
        assert isinstance(message, Ask)
        f(actor, sender, message.message, message.ref_id)
