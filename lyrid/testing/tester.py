from lyrid.base.actor import Actor
from .captor import Captor
from .probe import BackgroundTaskExecutorProbe, MessengerProbe
from .simulator import Simulator
from .. import Address, ActorProcess, ProcessContext
from ..common import UUID4Generator


class ActorTester:
    def __init__(self, actor: Actor):
        messenger = MessengerProbe()
        bg_task_executor = BackgroundTaskExecutorProbe()

        actor_address = Address("$.tester.actor")

        self._process = ActorProcess(actor)
        self.capture: Captor = Captor(actor_address, messenger, bg_task_executor)
        self.simulate: Simulator = Simulator(self._process)

        self._process.set_context(ProcessContext(
            actor_address, messenger, bg_task_executor, UUID4Generator(),
        ))
