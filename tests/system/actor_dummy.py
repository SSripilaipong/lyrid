from lyrid.core.actor import IActor
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger


class ActorDummy(IActor):
    def __init__(self, address: Address, messenger: IMessenger, supervisor_address: Address):
        pass

    def receive(self, sender: Address, message: Message):
        pass
