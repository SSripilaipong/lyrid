import uuid

from lyrid.core.common import IdGenerator


class UUID4Generator(IdGenerator):

    def generate(self) -> str:
        return uuid.uuid4().hex
