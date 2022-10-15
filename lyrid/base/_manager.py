from lyrid.core.manager import ITaskScheduler, ActorMessageDeliveryTask, ActorMessageSendingCommand, SpawnActorCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.processor import Command, IProcessor, ProcessorStartCommand, ProcessorStopCommand
from lyrid.core.system import ManagerSpawnActorMessage


class ManagerBase:
    def __init__(self, scheduler: ITaskScheduler, processor: IProcessor):
        self._scheduler = scheduler
        self._processor = processor

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, ManagerSpawnActorMessage):
            self._processor.process(SpawnActorCommand(address=message.address, type_=message.type_))
        else:
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
        elif isinstance(command, ProcessorStopCommand):
            self._scheduler.stop()
        else:
            raise NotImplementedError()
