from abc import ABC, ABCMeta
from dataclasses import dataclass
# noinspection PyUnresolvedReferences
from typing import Optional, Any, Callable, _ProtocolMeta

from lyrid.base import Actor
from lyrid.core.process import ProcessContext

ACTOR_KEYWORDS = ("address", "_address", "_messenger")


class _Empty:
    pass


class _Meta(_ProtocolMeta, ABCMeta):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)
        for keyword in ACTOR_KEYWORDS:
            if keyword in dct or keyword in dct.get("__annotations__", {}):
                raise NameError(f"Cannot assign field named '{keyword}'")
        return obj


class StatefulActor(Actor, ABC, metaclass=_Meta):
    def __init__(self, context: ProcessContext):
        super().__init__(context)

        for name, type_ in self.__annotations__.items():
            assert name not in ACTOR_KEYWORDS

            default_value = getattr(self, name, _Empty)
            if default_value == _Empty:
                raise NotImplementedError()

            if isinstance(default_value, Field):
                if default_value.default is not _Empty:
                    default_value = default_value.default
                elif default_value.default_factory is not None:
                    default_value = default_value.default_factory()
                else:
                    raise NotImplementedError()

            setattr(self, name, default_value)


@dataclass(frozen=True)
class Field:
    default: Optional[Any] = None
    default_factory: Optional[Callable[[], Any]] = None


def field(*, default: Any = _Empty, default_factory: Optional[Callable[[], Any]] = None) -> Any:
    return Field(default=default, default_factory=default_factory)
