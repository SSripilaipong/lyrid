from typing import Dict

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, IManager, RegisterAddressCommand, SendingCommand, \
    MessengerRegisterAddressMessage
from lyrid.core.processor import IProcessor, Command, ProcessorStartCommand, ProcessorStopCommand


class MessengerBase(IMessenger):
    def __init__(self, managers: Dict[Address, IManager], processor: IProcessor):
        self._managers = managers
        self._processor = processor
        self._address_to_manager: Dict[Address, IManager] = dict()

    def send(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, MessengerRegisterAddressMessage):
            self._processor.process(RegisterAddressCommand(
                address=message.address,
                manager_address=message.manager_address,
                requester_address=sender,
            ))
        else:
            self._processor.process(SendingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, SendingCommand):
            self._on_sending(command.sender, command.receiver, command.message)
        elif isinstance(command, RegisterAddressCommand):
            self._on_registering(command.address, command.manager_address)
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

    def _on_registering(self, address: Address, manager_address: Address):
        self._address_to_manager[address] = self._managers[manager_address]
