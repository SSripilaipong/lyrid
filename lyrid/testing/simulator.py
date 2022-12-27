from lyrid.base.actor import Actor
from lyrid.core.messaging import Message, Address


class Simulator:
    def __init__(self, actor: Actor):
        self._actor = actor

    def tell(self, message: Message, by: Address):
        self._actor.on_receive(by, message)
