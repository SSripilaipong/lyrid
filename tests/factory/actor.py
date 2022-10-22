from typing import TypeVar, Type

from lyrid import ActorBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock

T = TypeVar("T", bound=ActorBase)


def create_actor(type_: Type[T], *, address: Address = None, messenger: IMessenger = None,
                 supervisor_address: Address = None) -> T:
    address = address or Address("$")
    messenger = messenger or MessengerMock()
    supervisor_address = supervisor_address or Address("$.mommy")
    return type_(address, messenger, supervisor_address)
