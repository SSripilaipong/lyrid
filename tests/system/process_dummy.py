from lyrid import ProcessContext
from lyrid.core.messaging import Address, Message
from lyrid.core.process import Process


class ProcessDummyWithContext(Process):
    def __init__(self, context: ProcessContext):
        pass

    def receive(self, sender: Address, message: Message):
        pass


class ProcessDummy(Process):

    def receive(self, sender: Address, message: Message):
        pass
