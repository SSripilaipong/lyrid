from lyrid.base import ProcessorBase
from lyrid.core.processor import Command


def create_processor() -> ProcessorBase:
    return ProcessorBase(handle=handle_mock)


def handle_mock(_: Command):
    pass
