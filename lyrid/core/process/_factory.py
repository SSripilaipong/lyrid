from typing import Protocol

from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from lyrid.core.process import Process


class ProcessFactory(Protocol):
    def __call__(self, address: Address, messenger: IMessenger) -> Process: ...
