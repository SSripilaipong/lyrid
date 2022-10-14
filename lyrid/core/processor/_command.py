from dataclasses import dataclass


class Command:
    pass


@dataclass
class ProcessorStartCommand(Command):
    pass


class ProcessorStopCommand(Command):
    pass
