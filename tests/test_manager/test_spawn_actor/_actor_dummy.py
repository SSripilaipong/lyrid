from dataclasses import dataclass
from typing import TYPE_CHECKING

from lyrid.core.actor import IActor
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger


@dataclass
class MyActor(IActor):
    address: Address
    messenger: IMessenger

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, address: Address, messenger: IMessenger): ...
