from lyrid.base.actor import Actor
from .captor import Captor
from .mock import BackgroundTaskExecutorForTesting, MessengerForTesting, IdGeneratorForTesting
from .simulator import Simulator
from .. import Address, ActorProcess, ProcessContext


class ActorTester:
    def __init__(self, actor: Actor):
        messenger = MessengerForTesting()

        self._process = ActorProcess(actor)
        self.capture: Captor = Captor(messenger)
        self.simulate: Simulator = Simulator(self._process)

        self._process.set_context(ProcessContext(
            Address("$.tester.actor"), messenger, BackgroundTaskExecutorForTesting(), IdGeneratorForTesting(),
        ))
