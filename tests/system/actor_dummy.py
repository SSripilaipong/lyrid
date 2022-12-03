from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.process import Process


class ProcessDummy(Process):
    def __init__(self, address: Address, messenger: IMessenger, supervisor_address: Address):
        pass

    def receive(self, sender: Address, message: Message):
        pass
