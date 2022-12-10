from typing import List

from lyrid import Address
from lyrid.system import PlacementPolicy


class PlacementPolicyMock(PlacementPolicy):
    def __init__(self):
        self.set_node_addresses__addresses = None

    def set_node_addresses(self, addresses: List[Address]):
        self.set_node_addresses__addresses = addresses
