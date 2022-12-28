from contextlib import suppress

from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessStoppedSignal


class Simulator:
    def __init__(self, process: ActorProcess):
        self._process = process

    def tell(self, message: Message, by: Address):
        with suppress(ProcessStoppedSignal):
            self._process.receive(by, message)
