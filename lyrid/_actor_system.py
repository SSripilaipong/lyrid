import multiprocessing as mp
from typing import List, Tuple

from lyrid.base import ActorSystemBase, ThreadedTaskScheduler, QueueBasedMessenger, MultiProcessedCommandProcessingLoop, \
    ProcessManagingNode
from lyrid.base.background_task_executor import ThreadBackgroundTaskExecutor
from lyrid.base.messenger import MessengerCommandProcessor
from lyrid.common import BuiltinRandomizer, UUID4Generator, BuiltinThreadingClient
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import Messenger, Node
from lyrid.core.system import Placement


# noinspection PyPep8Naming
def ActorSystem(n_nodes: int = None, placement: List[Placement] = None) -> ActorSystemBase:
    messenger_address = Address("#messenger")

    messenger, messenger_processor, messenger_command_processor = _create_messenger(messenger_address)

    node_processors = []
    node_addresses = []
    for i in range(max(1, n_nodes or (mp.cpu_count() - 2))):
        address = Address(f"#node{i}")
        node, node_processor = _create_node(address, messenger)
        messenger_command_processor.add_node(address, node)
        node_processors.append(node_processor)
        node_addresses.append(address)

    system, system_processor = _create_actor_system(node_addresses, messenger, messenger_address,
                                                    placement=placement or [])
    messenger_command_processor.add_node(Address("$"), system)
    messenger_command_processor.initial_register_address(Address("$"), Address("$"))

    messenger_processor.start()
    for node_processor in node_processors:
        node_processor.start()
    system_processor.start()
    system.register_running_processors(node_processors + [messenger_processor, system_processor])

    return system


def _create_actor_system(node_addresses: List[Address], messenger: Messenger, messenger_address: Address,
                         placement: List[Placement]) \
        -> Tuple[ActorSystemBase, CommandProcessingLoop]:
    command_queue = mp.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    id_generator = UUID4Generator()
    randomizer = BuiltinRandomizer()
    reply_queue = mp.Manager().Queue()
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    background_task_executor = ThreadBackgroundTaskExecutor(BuiltinThreadingClient(), messenger)
    system = ActorSystemBase(scheduler=scheduler, processor=command_processor, messenger=messenger,
                             placements=placement, node_addresses=node_addresses, address=Address("$"),
                             messenger_address=messenger_address, reply_queue=reply_queue,
                             id_generator=id_generator, root_address=Address("$"), randomizer=randomizer,
                             background_task_executor=background_task_executor)
    command_processor.set_handle(system.handle_processor_command)

    return system, command_processor


def _create_messenger(address: Address) -> Tuple[Messenger, CommandProcessingLoop, MessengerCommandProcessor]:
    command_queue = mp.Manager().Queue()
    command_processor_loop = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    messenger = QueueBasedMessenger(address=address, command_queue=command_queue)
    command_processor = MessengerCommandProcessor(address=address, command_queue=command_queue)
    command_processor_loop.set_handle(command_processor.handle_command)

    return messenger, command_processor_loop, command_processor


def _create_node(address: Address, messenger: Messenger) -> Tuple[Node, CommandProcessingLoop]:
    command_queue = mp.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    background_task_executor = ThreadBackgroundTaskExecutor(BuiltinThreadingClient(), messenger)
    node = ProcessManagingNode(scheduler=scheduler, processor=command_processor, messenger=messenger,
                               address=address,
                               background_task_executor=background_task_executor,
                               id_generator=UUID4Generator())
    command_processor.set_handle(node.handle_processor_command)

    return node, command_processor
