from lyrid import Actor, ActorProcess
from lyrid.base.actor import ActorContext
from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.common import IdGenerator
from lyrid.core.messaging import Address
from lyrid.core.messenger import Messenger
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock


def create_actor_process(actor: Actor, *, address: Address = None, messenger: Messenger = None,
                         background_task_executor: BackgroundTaskExecutor = None,
                         id_gen: IdGenerator = None) -> ActorProcess:
    address = address or Address("$")
    messenger = messenger or MessengerMock()
    background_task_executor = background_task_executor or BackgroundTaskExecutorMock()
    id_gen = id_gen or IdGeneratorMock()

    process = ActorProcess(actor)
    process.set_context(ActorContext(
        address=address, messenger=messenger, background_task_executor=background_task_executor, id_generator=id_gen,
        next_actor=actor,
    ))
    return process
