from typing import TypeVar, Callable

FuncT = TypeVar("FuncT", bound=Callable[..., object])


def spawnable(actor: FuncT) -> FuncT:
    return actor
