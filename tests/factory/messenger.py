from typing import Dict

from lyrid.base import MessengerBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IManager
from lyrid.core.processor import IProcessor
from tests.mock.processor import ProcessorMock


def create_messenger(*, address: Address = None, managers: Dict[Address, IManager] = None,
                     processor: IProcessor = None) -> MessengerBase:
    address = address or Address("#default-messenger")
    managers = managers or dict()
    processor = processor or ProcessorMock()
    return MessengerBase(address, managers, processor)
