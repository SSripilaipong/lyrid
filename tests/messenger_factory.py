from typing import Dict

from lyrid import MessengerBase
from lyrid.core.messenger import IManager


def create_messenger_with_managers(managers: Dict[str, IManager]) -> MessengerBase:
    return MessengerBase(managers)
