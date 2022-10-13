from typing import Dict

from lyrid import MessengerBase
from lyrid.core.messenger import IManager
from lyrid.core.processor import IProcessor
from tests.processor_mock import ProcessorMock


def create_messenger(*, managers: Dict[str, IManager] = None, processor: IProcessor = None) -> MessengerBase:
    managers: Dict[str, IManager] = managers or dict()
    processor: IProcessor = processor or ProcessorMock()
    return MessengerBase(managers, processor)
