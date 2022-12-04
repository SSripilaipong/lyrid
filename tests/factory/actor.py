from typing import TypeVar, Type

from lyrid import VanillaActor
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock

A = TypeVar("A", bound=VanillaActor)


def create_actor(type_: Type[A], *, address: Address = None, messenger: IMessenger = None) -> A:
    address = address or Address("$")
    messenger = messenger or MessengerMock()
    return type_(address, messenger)
