import multiprocessing as mp
from typing import List, Tuple

from lyrid.base import ActorSystemBase, ThreadedTaskScheduler, MessengerBase, MultiProcessedCommandProcessingLoop, \
    ProcessManagingNode
from lyrid.common import UUID4Generator
from lyrid.common._randomizer import BuiltinRandomizer
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, Node


# noinspection PyPep8Naming
def ActorSystem(n_nodes: int = None) -> ActorSystemBase:
    messenger_address = Address("#messenger")

    messenger, messenger_processor = _create_messenger(messenger_address)

    node_processors = []
    node_addresses = []
    for i in range(max(1, n_nodes or (mp.cpu_count() - 2))):
        address = Address(f"#node{i}")
        _, node_processor = _create_node(address, messenger)
        node_processors.append(node_processor)
        node_addresses.append(address)

    system, system_processor = _create_actor_system(node_addresses, messenger, messenger_address,
                                                    processors=node_processors + [messenger_processor])

    for node in node_processors:
        node.start()
    messenger_processor.start()
    system_processor.start()

    return system


def _create_actor_system(node_addresses: List[Address], messenger: IMessenger, messenger_address: Address,
                         processors: List[CommandProcessingLoop]) \
        -> Tuple[ActorSystemBase, CommandProcessingLoop]:
    command_queue = mp.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    id_generator = UUID4Generator()
    randomizer = BuiltinRandomizer()
    reply_queue = mp.Manager().Queue()
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    system = ActorSystemBase(scheduler=scheduler, processor=command_processor, messenger=messenger,
                             node_addresses=node_addresses, address=Address("$"),
                             messenger_address=messenger_address, reply_queue=reply_queue,
                             id_generator=id_generator, root_address=Address("$"), randomizer=randomizer,
                             processors=processors + [command_processor])
    command_processor.set_handle(system.handle_processor_command)

    messenger.add_node(Address("$"), system)
    messenger.initial_register_address(Address("$"), Address("$"))
    return system, command_processor


def _create_messenger(address: Address) -> Tuple[IMessenger, CommandProcessingLoop]:
    command_queue = mp.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    messenger = MessengerBase(address=address, processor=command_processor)
    command_processor.set_handle(messenger.handle_processor_command)

    return messenger, command_processor


def _create_node(address: Address, messenger: IMessenger) -> Tuple[Node, CommandProcessingLoop]:
    command_queue = mp.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    node = ProcessManagingNode(scheduler=scheduler, processor=command_processor, messenger=messenger,
                               address=address)
    command_processor.set_handle(node.handle_processor_command)

    messenger.add_node(address, node)

    return node, command_processor
