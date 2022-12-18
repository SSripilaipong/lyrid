import queue
from queue import Queue
from typing import Dict

from lyrid.base import QueueBasedMessenger
from lyrid.base.messenger import MessengerCommandProcessor
from lyrid.core.messaging import Address
from lyrid.core.messenger import Node


def create_messenger(*, address: Address = None, nodes: Dict[Address, Node] = None,
                     command_queue: Queue = None) -> QueueBasedMessenger:
    address = address or Address("#default-messenger")
    command_queue = command_queue if command_queue is not None else queue.Queue()
    return QueueBasedMessenger(address=address, nodes=nodes, command_queue=command_queue)


def create_messenger_command_processor(*, address: Address = None, nodes: Dict[Address, Node] = None,
                                       command_queue: Queue = None) -> MessengerCommandProcessor:
    address = address or Address("#default-messenger")
    command_queue = command_queue or queue.Queue()
    return MessengerCommandProcessor(address=address, nodes=nodes, command_queue=command_queue)
