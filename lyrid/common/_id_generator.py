import uuid


class IdGenerator:

    @staticmethod
    def generate() -> str:
        return uuid.uuid4().hex
