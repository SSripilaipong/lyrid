from lyrid.base.actor import Actor, AbstractActor
from .captor import Captor
from .probe import BackgroundTaskExecutorProbe, MessengerProbe
from .simulator import Simulator
from .. import Address, ActorProcess, ProcessContext
from ..base.actor._status import ActorStatus
from ..common import UUID4Generator


class ActorTester:
    def __init__(self, actor: Actor):
        messenger = MessengerProbe()
        bg_task_executor = BackgroundTaskExecutorProbe()

        self._actor_address = Address("$.tester.actor")

        self._process = ActorProcess(actor)
        self.capture: Captor = Captor(self._actor_address, messenger, bg_task_executor)
        self.simulate: Simulator = Simulator(self._actor_address, self._process, self.capture)

        self._process.set_context(ProcessContext(
            self._actor_address, messenger, bg_task_executor, UUID4Generator(),
        ))

    @property
    def current_actor(self) -> AbstractActor:
        return self._process.actor

    @property
    def actor_address(self) -> Address:
        return self._actor_address

    def is_running(self) -> bool:
        return self._process.actor.context.status == ActorStatus.ACTIVE
