from abc import abstractmethod
from typing import Protocol, Callable

from lyrid.base.actor import Actor
from lyrid.core.messaging import Address, Message


class HandleRule(Protocol):
    @abstractmethod
    def match(self, sender: Address, message: Message) -> bool:
        pass

    @abstractmethod
    def execute(self, actor: Actor, sender: Address, message: Message):
        pass


class HandlePolicy(Protocol):

    @abstractmethod
    def create_handle_rule_with_function(self, function: Callable) -> HandleRule:
        pass
