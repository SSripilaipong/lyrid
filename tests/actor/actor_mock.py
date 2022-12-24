from dataclasses import dataclass
from typing import List

from lyrid import VanillaActor
from lyrid.core.messaging import Address, Message
from lyrid.core.process import ProcessContext


class MyActor(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        pass


class ChildActorWithContext(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        pass


class ChildActor(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        pass


@dataclass
class StopDummy(Message):
    pass


class WillStop(VanillaActor):
    def __init__(self, context: ProcessContext):
        super(WillStop, self).__init__(context)

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


class WillFail(VanillaActor):
    def __init__(self, context: ProcessContext):
        super(WillFail, self).__init__(context)

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
