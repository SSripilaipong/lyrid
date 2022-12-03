import queue
from typing import List

from lyrid.base import ActorSystemBase
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.common import IIdGenerator
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.node import TaskScheduler
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def create_actor_system(*, root_address: Address = None, address: Address = None, scheduler: TaskScheduler = None,
                        processor: CommandProcessingLoop = None,
                        messenger: IMessenger = None, reply_queue: queue.Queue = None,
                        manager_addresses: List[Address] = None, messenger_address: Address = None,
                        id_generator: IIdGenerator = None) -> ActorSystemBase:
    root_address = root_address or Address("$")
    address = address or Address("$")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    manager_addresses = manager_addresses or []
    messenger_address = messenger_address or Address("#default-messenger")
    reply_queue = reply_queue or queue.Queue()
    id_generator = id_generator or IdGeneratorMock()
    return ActorSystemBase(root_address=root_address, address=address, scheduler=scheduler, processor=processor,
                           messenger=messenger,
                           node_addresses=manager_addresses, messenger_address=messenger_address,
                           reply_queue=reply_queue, id_generator=id_generator)
