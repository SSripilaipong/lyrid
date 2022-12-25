from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process


class ProcessDummy(Process):

    def receive(self, sender: Address, message: Message):
        pass
