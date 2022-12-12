from typing import List, Optional

from lyrid import Address, PlacementPolicy
from lyrid.core.process import ProcessFactory
from lyrid.core.system import PlacementPolicyMatcher


class PlacementPolicyMock(PlacementPolicy):
    def __init__(self, get_placement_node__return: Address = None):
        self._get_placement_node__return = get_placement_node__return or Address("#none")

        self.set_node_addresses__addresses: Optional[List[Address]] = None

    def set_node_addresses(self, addresses: List[Address]):
        self.set_node_addresses__addresses = addresses

    def get_placement_node(self) -> Address:
        return self._get_placement_node__return


class PlacementPolicyMatcherMock(PlacementPolicyMatcher):
    def __init__(self, match__return: bool = False):
        self._match__return = match__return

        self.match__type: Optional[ProcessFactory] = None

    def match(self, type_: ProcessFactory) -> bool:
        self.match__type = type_
        return self._match__return
