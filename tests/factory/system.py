from typing import List

from lyrid.base import ActorSystemBase
from lyrid.core.manager import ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import IProcessor
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_actor_system(*, address: Address = None, scheduler: ITaskScheduler = None, processor: IProcessor = None,
                        messenger: IMessenger = None,
                        manager_addresses: List[Address] = None, messenger_address: Address = None) -> ActorSystemBase:
    address = address or Address("$")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    manager_addresses = manager_addresses or []
    messenger_address = messenger_address or Address("#default-messenger")
    return ActorSystemBase(address=address, scheduler=scheduler, processor=processor, messenger=messenger,
                           manager_addresses=manager_addresses, messenger_address=messenger_address)
