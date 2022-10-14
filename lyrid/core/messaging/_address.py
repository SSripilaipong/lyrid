from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    addr: str

    def child(self, key: str) -> 'Address':
        return Address(self.addr + '.' + key)

    def is_manager(self) -> bool:
        return self.addr.startswith("#")
