from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Message, Address


class Simulator:
    def __init__(self, process: ActorProcess):
        self._process = process

    def tell(self, message: Message, by: Address):
        self._process.receive(by, message)
