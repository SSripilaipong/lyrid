from dataclasses import dataclass, field
from typing import List, Optional

from lyrid import Actor
from lyrid.core.messaging import Address, Message


@dataclass
class ActorMockStop(Message):
    pass


@dataclass
class ActorMockFail(Message):
    exception: Exception


@dataclass
class ActorMock(Actor):
    name: Optional[str] = None
    on_stop__raise: Optional[Exception] = None

    on_receive__senders: List[Address] = field(default_factory=list, compare=False)
    on_receive__messages: List[Message] = field(default_factory=list, compare=False)
    on_stop__is_called: bool = False

    def on_receive(self, sender: Address, message: Message):
        self.on_receive__senders.append(sender)
        self.on_receive__messages.append(message)

        if isinstance(message, ActorMockFail):
            raise message.exception
        elif isinstance(message, ActorMockStop):
            self.stop()

    def on_stop(self):
        self.on_stop__is_called = True
        if self.on_stop__raise is not None:
            raise self.on_stop__raise

    def on_receive__clear_captures(self):
        self.on_receive__senders = []
        self.on_receive__messages = []
