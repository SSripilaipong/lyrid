from lyrid.core.manager import ITaskScheduler, ActorMessageDeliveryTask, ActorMessageSendingCommand, SpawnActorCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import Command, IProcessor, ProcessorStartCommand, ProcessorStopCommand
from lyrid.core.system import ManagerSpawnActorMessage, ManagerSpawnActorCompletedMessage


class ManagerBase:
    def __init__(self, address: Address, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger):
        self._address = address
        self._scheduler = scheduler
        self._processor = processor
        self._messenger = messenger

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, ManagerSpawnActorMessage):
            self._processor.process(SpawnActorCommand(address=message.address, type_=message.type_, reply_to=sender))
        else:
            self._processor.process(ActorMessageSendingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, ActorMessageSendingCommand):
            self._schedule_message_delivery(command)
        elif isinstance(command, ProcessorStartCommand):
            self._scheduler.start()
        elif isinstance(command, ProcessorStopCommand):
            self._scheduler.stop()
        elif isinstance(command, SpawnActorCommand):
            self._spawn_actor(command)
        else:
            raise NotImplementedError()

    def _spawn_actor(self, command: SpawnActorCommand):
        self._scheduler.register_actor(command.address, command.type_(command.address, self._messenger))
        reply_message = ManagerSpawnActorCompletedMessage(
            actor_address=command.address, manager_address=self._address,
        )
        self._messenger.send(self._address, command.reply_to, reply_message)

    def _schedule_message_delivery(self, command: ActorMessageSendingCommand):
        self._scheduler.schedule(ActorMessageDeliveryTask(
            target=command.receiver,
            message=command.message,
            sender=command.sender,
        ))
