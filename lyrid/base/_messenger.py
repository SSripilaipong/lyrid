from typing import Dict

from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, IManager, RegisterAddressCommand, SendingCommand
from lyrid.core.processor import IProcessor, Command, ProcessorStartCommand, ProcessorStopCommand


class MessengerBase(IMessenger):
    def __init__(self, managers: Dict[str, IManager], processor: IProcessor):
        self._managers = managers
        self._processor = processor
        self._addr_to_manager: Dict[Address, IManager] = dict()

    def send(self, sender: Address, receiver: Address, message: Message):
        self._processor.process(SendingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, SendingCommand):
            self._on_sending(command.sender, command.receiver, command.message)
        elif isinstance(command, RegisterAddressCommand):
            self._on_registering(command.addr, command.manager_key)
        elif isinstance(command, (ProcessorStartCommand, ProcessorStopCommand)):
            pass
        else:
            raise NotImplementedError()

    def _on_sending(self, sender: Address, receiver: Address, message: Message):
        self._addr_to_manager[receiver].handle_message(sender, receiver, message)

    def _on_registering(self, addr: Address, manager_key: str):
        self._addr_to_manager[addr] = self._managers[manager_key]
