import queue
from typing import Any, Iterator


def iter_until_empty(q: queue.Queue) -> Iterator[Any]:
    while True:
        try:
            yield q.get(block=False)
        except queue.Empty:
            break
