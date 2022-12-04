import random

from lyrid.core.common import Randomizer


class BuiltinRandomizer(Randomizer):

    def randrange(self, n: int) -> int:
        return random.randrange(n)
