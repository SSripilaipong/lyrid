from dataclasses import dataclass
from typing import TYPE_CHECKING

from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process, ProcessContext


@dataclass
class MyProcess(Process):
    context: ProcessContext

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, context: ProcessContext):
            pass
