from queue import Queue
from typing import Dict

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import Messenger, Node, RegisterAddressCommand, SendingCommand, \
    MessengerRegisterAddressMessage, SendingToNodeCommand, MessengerCommand


class QueueBasedMessenger(Messenger):
    def __init__(self, address: Address, command_queue: Queue, nodes: Dict[Address, Node] = None):
        self._address = address
        self._command_queue = command_queue

        self._nodes = nodes or dict()
        self._address_to_node: Dict[Address, Node] = dict()
        self._address_to_node_address: Dict[Address, Address] = dict()

    def send(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, MessengerRegisterAddressMessage):
            cmd: MessengerCommand = RegisterAddressCommand(
                address=message.address,
                node_address=message.node_address,
                requester_address=sender,
                ref_id=message.ref_id,
            )
        else:
            cmd = SendingCommand(sender=sender, receiver=receiver, message=message)
        self._command_queue.put(cmd)

    def send_to_node(self, sender: Address, of: Address, message: Message):
        cmd = SendingToNodeCommand(sender=sender, of=of, message=message)
        self._command_queue.put(cmd)
