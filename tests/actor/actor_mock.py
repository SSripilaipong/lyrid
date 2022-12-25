from dataclasses import dataclass
from typing import List

from lyrid import AbstractActor
from lyrid.core.messaging import Address, Message


class MyActor(AbstractActor):

    def on_receive(self, sender: Address, message: Message):
        pass


class ChildActor(AbstractActor):

    def on_receive(self, sender: Address, message: Message):
        pass


@dataclass
class StopDummy(Message):
    pass


class WillStop(AbstractActor):
    def __init__(self):
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


@dataclass
class FailDummy(Message):
    exception: Exception


class WillFail(AbstractActor):
    def __init__(self):
        self.on_receive__senders: List[Address] = []
        self.on_receive__messages: List[Message] = []

        self.on_stop__is_called = False

    def on_receive(self, sender: Address, message: Message):
        self.on_receive__senders.append(sender)
        self.on_receive__messages.append(message)

        if isinstance(message, FailDummy):
            raise message.exception

    def on_stop(self):
        self.on_stop__is_called = True

    def on_receive__clear_captures(self):
        self.on_receive__senders = []
        self.on_receive__messages = []
