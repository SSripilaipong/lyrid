from lyrid.base._command import ActorMessageSendingCommand
from lyrid.core.manager import ITaskScheduler, ActorTask
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command


class ManagerBase:
    def __init__(self, scheduler: ITaskScheduler):
        self._scheduler = scheduler

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        pass

    def handle_processor_command(self, command: Command):
        if isinstance(command, ActorMessageSendingCommand):
            self._scheduler.schedule(ActorTask(
                target=command.receiver,
                message=command.message,
                sender=command.sender,
            ))
        else:
            raise NotImplementedError()
