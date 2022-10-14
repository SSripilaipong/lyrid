from lyrid.core.manager import ITaskScheduler, ActorMessageDeliveryTask, ActorMessageSendingCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command, IProcessor, ProcessorStartCommand


class ManagerBase:
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor):
        self._scheduler = scheduler
        self._processor = processor

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        self._processor.process(ActorMessageSendingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, ActorMessageSendingCommand):
            self._scheduler.schedule(ActorMessageDeliveryTask(
                target=command.receiver,
                message=command.message,
                sender=command.sender,
            ))
        elif isinstance(command, ProcessorStartCommand):
            self._scheduler.start()
        else:
            raise NotImplementedError()
