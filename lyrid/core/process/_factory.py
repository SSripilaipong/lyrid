from typing import Protocol

from ._context import ProcessContext
from ._process import Process


class ProcessFactory(Protocol):
    def __call__(self, context: ProcessContext) -> Process: ...
