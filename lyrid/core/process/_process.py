from abc import abstractmethod
from typing import Protocol

from lyrid.core.messaging import Address, Message
from ._context import ProcessContext


class Process(Protocol):

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass

    def set_context(self, context: ProcessContext):
        return None
