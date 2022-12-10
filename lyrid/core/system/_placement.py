from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, List

from lyrid.core.messaging import Address


class PlacementPolicyMatcher(Protocol):
    pass


class PlacementPolicy(Protocol):

    @abstractmethod
    def set_node_addresses(self, addresses: List[Address]):
        pass


@dataclass
class Placement:
    match: PlacementPolicyMatcher
    policy: PlacementPolicy
