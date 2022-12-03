from dataclasses import dataclass
from typing import TYPE_CHECKING

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.process import Process


@dataclass
class MyProcess(Process):
    address: Address
    messenger: IMessenger

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, address: Address, messenger: IMessenger): ...
