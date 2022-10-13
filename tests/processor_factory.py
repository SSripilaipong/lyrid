from typing import Callable

from lyrid.base import ProcessorBase
from lyrid.core.processor import Command


def create_processor(handle: Callable[[Command], None]) -> ProcessorBase:
    return ProcessorBase(handle=handle)
