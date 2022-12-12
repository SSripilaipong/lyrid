import random
from typing import List

from lyrid.core.messaging import Address
from lyrid.core.system import PlacementPolicy


class RoundRobin(PlacementPolicy):
    def __init__(self):
        self._addresses = []
        self._index = 0
        self._n = 0

    def set_node_addresses(self, addresses: List[Address]):
        self._addresses = addresses.copy()
        self._index = 0
        self._n = len(self._addresses)

        random.shuffle(self._addresses)

    def get_placement_node(self) -> Address:
        node = self._addresses[self._index]
        self._index += 1
        if self._index >= self._n:
            self._index = 0
        return node
