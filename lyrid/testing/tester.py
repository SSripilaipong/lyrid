from lyrid.base.actor import Actor
from .captor import Captor
from .mock import BackgroundTaskExecutorForTesting, MessengerForTesting, IdGeneratorForTesting
from .simulator import Simulator
from .. import Address, ActorProcess, ProcessContext


class ActorTester:
    def __init__(self, actor: Actor):
        messenger = MessengerForTesting()
        bg_task_executor = BackgroundTaskExecutorForTesting()

        self._process = ActorProcess(actor)
        self.capture: Captor = Captor(messenger, bg_task_executor)
        self.simulate: Simulator = Simulator(self._process)

        self._process.set_context(ProcessContext(
            Address("$.tester.actor"), messenger, bg_task_executor, IdGeneratorForTesting(),
        ))
