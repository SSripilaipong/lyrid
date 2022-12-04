from dataclasses import dataclass
from typing import List

from lyrid import VanillaActor
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger


class MyActor(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        pass


class ChildActor(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        pass


@dataclass
class StopDummy(Message):
    pass


class WillStop(VanillaActor):
    def __init__(self, address: Address, messenger: IMessenger):
        super(WillStop, self).__init__(address, messenger)

        self.on_receive__senders: List[Address] = []
        self.on_receive__messages: List[Message] = []

        self.on_stop__is_called = False

    def on_receive(self, sender: Address, message: Message):
        self.on_receive__senders.append(sender)
        self.on_receive__messages.append(message)

        if message == StopDummy():
            self.stop()

    def on_stop(self):
        self.on_stop__is_called = True

    def on_receive__clear_captures(self):
        self.on_receive__senders = []
        self.on_receive__messages = []
