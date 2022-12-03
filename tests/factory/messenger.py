from typing import Dict

from lyrid.base import MessengerBase
from lyrid.core.command_processing_loop import CommandProcessingLoop
from lyrid.core.messaging import Address
from lyrid.core.messenger import IManager
from tests.mock.processor import ProcessorMock


def create_messenger(*, address: Address = None, managers: Dict[Address, IManager] = None,
                     processor: CommandProcessingLoop = None) -> MessengerBase:
    address = address or Address("#default-messenger")
    processor = processor or ProcessorMock()
    return MessengerBase(address=address, processor=processor, managers=managers)
