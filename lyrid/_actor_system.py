import multiprocessing
from typing import List, Tuple

from lyrid.base import ActorSystemBase, TaskSchedulerBase, MessengerBase, ProcessorBase, ManagerBase
from lyrid.common import IdGenerator
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger, IManager
from lyrid.core.processor import IProcessor


# noinspection PyPep8Naming
def ActorSystem() -> ActorSystemBase:
    messenger_address = Address("#messenger")

    messenger, messenger_processor = _create_messenger(messenger_address)

    _, manager_processor = _create_manager(Address("#manager1"), messenger)

    manager_addresses = [Address("#manager1")]

    system, system_processor = _create_actor_system(manager_addresses, messenger, messenger_address,
                                                    processors=[manager_processor, messenger_processor])

    manager_processor.start()
    messenger_processor.start()
    system_processor.start()

    return system


def _create_actor_system(manager_addresses: List[Address], messenger: IMessenger, messenger_address: Address,
                         processors: List[IProcessor]) \
        -> Tuple[ActorSystemBase, IProcessor]:
    command_queue = multiprocessing.Manager().Queue()
    processor = ProcessorBase(command_queue=command_queue)
    id_generator = IdGenerator()
    reply_queue = multiprocessing.Manager().Queue()
    scheduler = TaskSchedulerBase(messenger=messenger)
    system = ActorSystemBase(scheduler=scheduler, processor=processor, messenger=messenger,
                             manager_addresses=manager_addresses, address=Address("$"),
                             messenger_address=messenger_address, reply_queue=reply_queue,
                             id_generator=id_generator, root_address=Address("$"), processors=processors + [processor])
    processor.set_handle(system.handle_processor_command)

    messenger.add_manager(Address("$"), system)
    messenger.initial_register_address(Address("$"), Address("$"))
    return system, processor


def _create_messenger(address: Address) -> Tuple[IMessenger, IProcessor]:
    command_queue = multiprocessing.Manager().Queue()
    processor = ProcessorBase(command_queue=command_queue)
    messenger = MessengerBase(address=address, processor=processor)
    processor.set_handle(messenger.handle_processor_command)

    return messenger, processor


def _create_manager(address: Address, messenger: IMessenger) -> Tuple[IManager, IProcessor]:
    command_queue = multiprocessing.Manager().Queue()
    processor = ProcessorBase(command_queue=command_queue)
    scheduler = TaskSchedulerBase(messenger=messenger)
    manager = ManagerBase(scheduler=scheduler, processor=processor, messenger=messenger,
                          address=address)
    processor.set_handle(manager.handle_processor_command)

    messenger.add_manager(address, manager)

    return manager, processor
