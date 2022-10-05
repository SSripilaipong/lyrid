from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    addr: str
