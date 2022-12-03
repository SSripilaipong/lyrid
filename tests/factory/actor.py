from typing import TypeVar, Type

from lyrid import Actor
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock

T = TypeVar("T", bound=Actor)


def create_actor(type_: Type[T], *, address: Address = None, messenger: IMessenger = None) -> T:
    address = address or Address("$")
    messenger = messenger or MessengerMock()
    return type_(address, messenger)
