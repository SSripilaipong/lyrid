from abc import abstractmethod, ABC

from lyrid.core.messaging import Address, Message
from ._context import ProcessContext


class Process(ABC):

    @abstractmethod
    def receive(self, sender: Address, message: Message):
        pass

    def set_context(self, context: ProcessContext):
        return None
