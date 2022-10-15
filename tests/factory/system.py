from typing import List

from lyrid.base import ActorSystemBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_actor_system(*, messenger: IMessenger = None, manager_addresses: List[Address] = None) -> ActorSystemBase:
    scheduler = SchedulerMock()
    processor = ProcessorMock()
    messenger = messenger or MessengerMock()
    manager_addresses = manager_addresses or []
    return ActorSystemBase(scheduler=scheduler, processor=processor, messenger=messenger,
                           manager_addresses=manager_addresses)
