import queue
from typing import List

from lyrid.base import ActorSystemBase
from lyrid.core.background_task import BackgroundTaskExecutor
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.common import IdGenerator, Randomizer
from lyrid.core.messaging import Address
from lyrid.core.messenger import Messenger
from lyrid.core.node import TaskScheduler
from lyrid.core.system import Placement
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.randomizer import RandomizerMock
from tests.mock.scheduler import SchedulerMock


def create_actor_system(*, root_address: Address = None, address: Address = None, scheduler: TaskScheduler = None,
                        processor: CommandProcessingLoop = None,
                        messenger: Messenger = None, reply_queue: queue.Queue = None,
                        placements: List[Placement] = None, node_addresses: List[Address] = None,
                        messenger_address: Address = None, id_generator: IdGenerator = None,
                        randomizer: Randomizer = None,
                        background_task_executor: BackgroundTaskExecutor = None) -> ActorSystemBase:
    root_address = root_address or Address("$")
    address = address or Address("$")
    scheduler = scheduler or SchedulerMock()
    processor = processor or ProcessorMock()
    messenger = messenger or MessengerMock()
    placements = placements or []
    node_addresses = node_addresses or []
    messenger_address = messenger_address or Address("#default-messenger")
    reply_queue = reply_queue or queue.Queue()
    id_generator = id_generator or IdGeneratorMock()
    randomizer = randomizer or RandomizerMock()
    background_task_executor = background_task_executor or BackgroundTaskExecutorMock()
    return ActorSystemBase(root_address=root_address, address=address, scheduler=scheduler, processor=processor,
                           messenger=messenger, placements=placements,
                           node_addresses=node_addresses, messenger_address=messenger_address,
                           reply_queue=reply_queue, id_generator=id_generator, randomizer=randomizer,
                           background_task_executor=background_task_executor)
