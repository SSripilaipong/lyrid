from dataclasses import dataclass

from lyrid import ActorBase
from lyrid.core.messaging import Address, Message


class MyActor(ActorBase):

    def on_receive(self, sender: Address, message: Message):
        pass


class ChildActor(ActorBase):

    def on_receive(self, sender: Address, message: Message):
        pass


@dataclass
class StopDummy(Message):
    pass


class WillStop(ActorBase):
    def on_receive(self, sender: Address, message: Message):
        if message == StopDummy():
            self.stop()
