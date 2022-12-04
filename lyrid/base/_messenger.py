from typing import Dict

from lyrid.core.command_processing_loop import CommandProcessingLoop, Command, ProcessorStartCommand, \
    ProcessorStopCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, Node, RegisterAddressCommand, SendingCommand, \
    MessengerRegisterAddressMessage, MessengerRegisterAddressCompletedMessage, SendingToManagerCommand


class MessengerBase(IMessenger):
    def __init__(self, address: Address, processor: CommandProcessingLoop, nodes: Dict[Address, Node] = None):
        self._address = address
        self._processor = processor
        self._nodes = nodes or dict()
        self._address_to_node: Dict[Address, Node] = dict()
        self._address_to_node_address: Dict[Address, Address] = dict()

    def add_node(self, address: Address, node: Node):
        self._nodes[address] = node

    def send(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, MessengerRegisterAddressMessage):
            self._processor.process(RegisterAddressCommand(
                address=message.address,
                node_address=message.node_address,
                requester_address=sender,
                ref_id=message.ref_id,
            ))
        else:
            self._processor.process(SendingCommand(sender=sender, receiver=receiver, message=message))

    def send_to_node(self, sender: Address, of: Address, message: Message):
        self._processor.process(SendingToManagerCommand(sender=sender, of=of, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, SendingCommand):
            self._on_sending(command.sender, command.receiver, command.message)
        elif isinstance(command, SendingToManagerCommand):
            self._on_sending_to_manager(command.sender, command.of, command.message)
        elif isinstance(command, RegisterAddressCommand):
            self._on_registering(command)
        elif isinstance(command, (ProcessorStartCommand, ProcessorStopCommand)):
            pass
        else:
            raise NotImplementedError()

    def _on_sending(self, sender: Address, receiver: Address, message: Message):
        if receiver.is_manager():
            node = self._nodes.get(receiver, None)
        else:
            node = self._address_to_node.get(receiver, None)
        if node is None:
            return
        node.handle_message(sender, receiver, message)

    def _on_sending_to_manager(self, sender: Address, of: Address, message: Message):
        manager_address = self._address_to_node_address[of]
        manager = self._nodes[manager_address]
        manager.handle_message(sender, manager_address, message)

    def _on_registering(self, command: RegisterAddressCommand):
        self.initial_register_address(command.address, command.node_address)
        self._processor.process(SendingCommand(
            sender=self._address,
            receiver=command.requester_address,
            message=MessengerRegisterAddressCompletedMessage(
                address=command.address,
                manager_address=command.node_address,
                ref_id=command.ref_id,
            )
        ))

    def initial_register_address(self, actor_address: Address, node_address: Address):
        self._address_to_node[actor_address] = self._nodes[node_address]
        self._address_to_node_address[actor_address] = node_address
