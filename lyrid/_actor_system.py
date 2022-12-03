import multiprocessing
from typing import List, Tuple

from lyrid.base import ActorSystemBase, ThreadedTaskScheduler, MessengerBase, MultiProcessedCommandProcessingLoop, \
    ProcessManagingNode
from lyrid.common import IdGenerator
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, Node


# noinspection PyPep8Naming
def ActorSystem() -> ActorSystemBase:
    messenger_address = Address("#messenger")

    messenger, messenger_processor = _create_messenger(messenger_address)

    _, manager_processor = _create_node(Address("#manager1"), messenger)

    manager_addresses = [Address("#manager1")]

    system, system_processor = _create_actor_system(manager_addresses, messenger, messenger_address,
                                                    processors=[manager_processor, messenger_processor])

    manager_processor.start()
    messenger_processor.start()
    system_processor.start()

    return system


def _create_actor_system(manager_addresses: List[Address], messenger: IMessenger, messenger_address: Address,
                         processors: List[CommandProcessingLoop]) \
        -> Tuple[ActorSystemBase, CommandProcessingLoop]:
    command_queue = multiprocessing.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    id_generator = IdGenerator()
    reply_queue = multiprocessing.Manager().Queue()
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    system = ActorSystemBase(scheduler=scheduler, processor=command_processor, messenger=messenger,
                             manager_addresses=manager_addresses, address=Address("$"),
                             messenger_address=messenger_address, reply_queue=reply_queue,
                             id_generator=id_generator, root_address=Address("$"),
                             processors=processors + [command_processor])
    command_processor.set_handle(system.handle_processor_command)

    messenger.add_node(Address("$"), system)
    messenger.initial_register_address(Address("$"), Address("$"))
    return system, command_processor


def _create_messenger(address: Address) -> Tuple[IMessenger, CommandProcessingLoop]:
    command_queue = multiprocessing.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    messenger = MessengerBase(address=address, processor=command_processor)
    command_processor.set_handle(messenger.handle_processor_command)

    return messenger, command_processor


def _create_node(address: Address, messenger: IMessenger) -> Tuple[Node, CommandProcessingLoop]:
    command_queue = multiprocessing.Manager().Queue()
    command_processor = MultiProcessedCommandProcessingLoop(command_queue=command_queue)
    scheduler = ThreadedTaskScheduler(messenger=messenger)
    manager = ProcessManagingNode(scheduler=scheduler, processor=command_processor, messenger=messenger,
                                  address=address)
    command_processor.set_handle(manager.handle_processor_command)

    messenger.add_node(address, manager)

    return manager, command_processor
