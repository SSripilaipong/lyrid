from typing import List

from lyrid.base import ActorSystemBase
from lyrid.core.messaging import Address
from lyrid.core.messenger import IMessenger


def create_actor_system(messenger: IMessenger, manager_addresses: List[Address]) -> ActorSystemBase:
    return ActorSystemBase(messenger=messenger, manager_addresses=manager_addresses)
