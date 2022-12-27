from lyrid.base.actor import Actor
from .simulator import Simulator


class ActorTester:
    def __init__(self, actor: Actor):
        self.simulate = Simulator(actor)
