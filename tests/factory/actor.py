from typing import TypeVar, Type

from lyrid import VanillaActor
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.process import BackgroundTaskExecutor, ProcessContext
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.messenger import MessengerMock

A = TypeVar("A", bound=VanillaActor)


def create_actor(type_: Type[A], *, address: Address = None, messenger: IMessenger = None,
                 background_task_executor: BackgroundTaskExecutor = None) -> A:
    address = address or Address("$")
    messenger = messenger or MessengerMock()
    background_task_executor = background_task_executor or BackgroundTaskExecutorMock()
    return type_(ProcessContext(
        address=address, messenger=messenger, background_task_executor=background_task_executor,
    ))
