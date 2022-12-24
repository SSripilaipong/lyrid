from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, List, Type

from lyrid.core.messaging import Address
from lyrid.core.process import Process


class PlacementPolicyMatcher(Protocol):

    @abstractmethod
    def match(self, type_: Type[Process]) -> bool:
        pass


class PlacementPolicy(Protocol):

    @abstractmethod
    def set_node_addresses(self, addresses: List[Address]):
        pass

    @abstractmethod
    def get_placement_node(self) -> Address:
        pass


@dataclass
class Placement:
    match: PlacementPolicyMatcher
    policy: PlacementPolicy
