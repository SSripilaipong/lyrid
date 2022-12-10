from typing import List

from lyrid import Address
from lyrid.core.process import ProcessFactory
from lyrid.core.system import PlacementPolicyMatcher
from lyrid.system import PlacementPolicy


class PlacementPolicyMock(PlacementPolicy):
    def __init__(self):
        self.set_node_addresses__addresses = None

    def set_node_addresses(self, addresses: List[Address]):
        self.set_node_addresses__addresses = addresses


class PlacementPolicyMatcherMock(PlacementPolicyMatcher):
    def __init__(self):
        self.match__type = None

    def match(self, type_: ProcessFactory) -> bool:
        self.match__type = type_
        return False
