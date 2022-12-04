from typing import Optional

from lyrid.core.common import Randomizer


class RandomizerMock(Randomizer):
    def __init__(self, randrange__return: int = None):
        self.randrange__n: Optional[int] = None
        self._randrange__return: Optional[int] = randrange__return

    def randrange(self, n: int) -> int:
        self.randrange__n = n
        return self._randrange__return or 0
