from typing import Dict

from lyrid.base import MessengerBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IManager
from lyrid.core.processor import IProcessor
from tests.mock.processor import ProcessorMock


def create_messenger(*, managers: Dict[Address, IManager] = None, processor: IProcessor = None) -> MessengerBase:
    managers = managers or dict()
    processor = processor or ProcessorMock()
    return MessengerBase(managers, processor)
