from typing import Protocol

from lyrid.core.actor import IActor
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger


class IActorFactory(Protocol):
    def __call__(self, address: Address, messenger: IMessenger) -> IActor: ...
