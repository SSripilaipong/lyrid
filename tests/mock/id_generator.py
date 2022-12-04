from lyrid.core.common import IdGenerator


class IdGeneratorMock(IdGenerator):
    def __init__(self, generate__return: str = ""):
        self._generate__return = generate__return

    def generate(self) -> str:
        return self._generate__return
