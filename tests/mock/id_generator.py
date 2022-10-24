class IdGeneratorMock:
    def __init__(self, generate__return: str = ""):
        self._generate__return = generate__return

    def generate(self) -> str:
        return self._generate__return
