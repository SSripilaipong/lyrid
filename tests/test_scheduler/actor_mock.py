from typing import Optional, List

from lyrid import ActorBase
from lyrid.core.actor import ActorStoppedSignal
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger


class MyActor(ActorBase):
    def __init__(self, address: Address, messenger: IMessenger):
        super().__init__(address=address, messenger=messenger)

        self.receive__sender: Optional[Address] = None
        self.receive__message: Optional[Message] = None

    def receive(self, sender: Address, message: Message):
        self.receive__sender = sender
        self.receive__message = message


class WillStop(ActorBase):
    def __init__(self, address: Address, messenger: IMessenger):
        super().__init__(address=address, messenger=messenger)

        self.receive__senders: List[Address] = []
        self.receive__messages: List[Message] = []

    def receive(self, sender: Address, message: Message):
        self.receive__senders.append(sender)
        self.receive__messages.append(message)
        raise ActorStoppedSignal()
