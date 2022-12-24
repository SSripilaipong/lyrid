from dataclasses import dataclass, field
from typing import Set, Optional

from lyrid.core.messaging import Address
from lyrid.core.process import ProcessContext, ChildStopped
from ._status import ActorStatus


@dataclass
class ActorContext(ProcessContext):
    system_address: Address = Address("$")
    status: str = ActorStatus.ACTIVE

    active_children: Set[Address] = field(default_factory=set)
    stopped_message_to_report: Optional[ChildStopped] = None
