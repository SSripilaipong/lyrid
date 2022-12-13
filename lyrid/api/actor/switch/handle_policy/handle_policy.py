from abc import abstractmethod
from typing import Protocol, Callable

from lyrid.base import Actor
from lyrid.core.messaging import Address, Message


class HandlePolicy(Protocol):
    @abstractmethod
    def matches(self, sender: Address, message: Message) -> bool:
        pass

    @abstractmethod
    def decorate(self, f: Callable) -> Callable:
        pass

    @abstractmethod
    def execute(self, f: Callable, actor: Actor, sender: Address, message: Message):
        pass
