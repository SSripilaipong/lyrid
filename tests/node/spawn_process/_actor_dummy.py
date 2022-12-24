from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process, ProcessContext


@dataclass
class MyProcessWithContext(Process):
    context: ProcessContext

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, context: ProcessContext):
            pass


@dataclass
class MyProcess(Process):
    set_context__context: Optional[ProcessContext] = None

    def set_context(self, context: ProcessContext):
        self.set_context__context = context

    def receive(self, sender: Address, message: Message):
        pass
