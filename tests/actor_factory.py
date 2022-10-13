from typing import TypeVar, Type

from lyrid import ActorBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger

T = TypeVar("T", bound=ActorBase)


def create_actor_with_address_and_messenger(type_: Type[T], address: Address, messenger: IMessenger) -> T:
    return type_(address, messenger)
