from typing import TypeVar, Type

from lyrid import ActorBase
from lyrid.core.messenger import IMessenger, Address

T = TypeVar("T", bound=ActorBase)


def create_actor_with_address_and_messenger(type_: Type[T], address: Address, messenger: IMessenger) -> T:
    return type_(address, messenger)
