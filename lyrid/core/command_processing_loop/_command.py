from dataclasses import dataclass


class Command:
    pass


@dataclass
class ProcessorStartCommand(Command):
    pass


@dataclass
class ProcessorStopCommand(Command):
    pass
