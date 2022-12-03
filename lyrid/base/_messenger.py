from typing import Dict

from lyrid.core.command_processing_loop import CommandProcessingLoop, Command, ProcessorStartCommand, \
    ProcessorStopCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, IManager, RegisterAddressCommand, SendingCommand, \
    MessengerRegisterAddressMessage, MessengerRegisterAddressCompletedMessage, SendingToManagerCommand


class MessengerBase(IMessenger):
    def __init__(self, address: Address, processor: CommandProcessingLoop, managers: Dict[Address, IManager] = None):
        self._address = address
        self._processor = processor
        self._managers = managers or dict()
        self._address_to_manager: Dict[Address, IManager] = dict()
        self._address_to_manager_address: Dict[Address, Address] = dict()

    def add_manager(self, address: Address, manager: IManager):
        self._managers[address] = manager

    def send(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, MessengerRegisterAddressMessage):
            self._processor.process(RegisterAddressCommand(
                address=message.address,
                manager_address=message.manager_address,
                requester_address=sender,
                ref_id=message.ref_id,
            ))
        else:
            self._processor.process(SendingCommand(sender=sender, receiver=receiver, message=message))

    def send_to_manager(self, sender: Address, of: Address, message: Message):
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
            manager = self._managers[receiver]
        else:
            manager = self._address_to_manager[receiver]
        manager.handle_message(sender, receiver, message)

    def _on_sending_to_manager(self, sender: Address, of: Address, message: Message):
        manager_address = self._address_to_manager_address[of]
        manager = self._managers[manager_address]
        manager.handle_message(sender, manager_address, message)

    def _on_registering(self, command: RegisterAddressCommand):
        self.initial_register_address(command.address, command.manager_address)
        self._processor.process(SendingCommand(
            sender=self._address,
            receiver=command.requester_address,
            message=MessengerRegisterAddressCompletedMessage(
                address=command.address,
                manager_address=command.manager_address,
                ref_id=command.ref_id,
            )
        ))

    def initial_register_address(self, actor_address: Address, manager_address: Address):
        self._address_to_manager[actor_address] = self._managers[manager_address]
        self._address_to_manager_address[actor_address] = manager_address
