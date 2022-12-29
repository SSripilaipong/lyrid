import uuid
from contextlib import suppress

from lyrid import Ask, BackgroundTaskExited
from lyrid.base.actor import ActorProcess
from lyrid.core.messaging import Message, Address
from lyrid.core.process import ProcessStoppedSignal
from .background_task import BackgroundTask


class Simulator:
    def __init__(self, actor_address: Address, process: ActorProcess):
        self._actor_address = actor_address
        self._process = process

    def tell(self, message: Message, by: Address):
        with suppress(ProcessStoppedSignal):
            self._process.receive(by, message)

    def ask(self, message: Message) -> str:
        ref_id = uuid.uuid4().hex
        self._process.receive(Address("$"), Ask(message, ref_id=ref_id))
        return ref_id

    def run_background_task(self, background_task: BackgroundTask):
        return_value = background_task.task(*background_task.args)
        self._process.receive(self._actor_address, BackgroundTaskExited(background_task.task_id, return_value))
