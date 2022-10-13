from typing import Dict

from lyrid.core.messenger import IMessenger, Address, Message, IManager


class MessengerBase(IMessenger):
    def __init__(self, managers: Dict[str, IManager]):
        self._managers = managers
        self._addr_to_manager: Dict[Address, IManager] = dict()

    def send(self, sender: Address, receiver: Address, message: Message):
        pass

    def on_sending(self, sender: Address, receiver: Address, message: Message):
        self._addr_to_manager[receiver].handle(sender, receiver, message)

    def on_registering(self, addr: Address, manager_key: str):
        self._addr_to_manager[addr] = self._managers[manager_key]
