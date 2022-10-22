from lyrid import ActorBase
from lyrid.core.actor import ActorStoppedSignal
from lyrid.core.messaging import Address, Message


class MyActor(ActorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.receive__sender = None
        self.receive__message = None

    def receive(self, sender: Address, message: Message):
        self.receive__sender = sender
        self.receive__message = message


class WillStop(ActorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.receive__senders = []
        self.receive__messages = []

    def receive(self, sender: Address, message: Message):
        self.receive__senders.append(sender)
        self.receive__messages.append(message)
        raise ActorStoppedSignal()
