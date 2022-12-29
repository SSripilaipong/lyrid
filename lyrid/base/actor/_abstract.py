from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Set, Optional

from lyrid.core.messaging import Address
from lyrid.core.messaging import Message
from lyrid.core.process import ProcessContext, ChildStopped
from ._status import ActorStatus


@dataclass
class ActorContext(ProcessContext):
    next_actor: 'AbstractActor'
    system_address: Address = Address("$")
    status: str = ActorStatus.ACTIVE

    active_children: Set[Address] = field(default_factory=set)
    stopped_message_to_report: Optional[ChildStopped] = None


class AbstractActor(ABC):
    _context: ActorContext

    @abstractmethod
    def on_receive(self, sender: Address, message: Message):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @property
    def context(self) -> ActorContext:
        return self._context

    def set_context(self, context: ActorContext):
        self._context = context
