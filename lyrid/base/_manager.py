from lyrid.core.actor import SupervisorForceStop
from lyrid.core.manager import (
    ITaskScheduler, ActorMessageDeliveryTask, MessageHandlingCommand, SpawnActorCommand, ManagerSpawnActorMessage,
    ManagerSpawnActorCompletedMessage,
)
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, IManager
from lyrid.core.processor import Command, IProcessor, ProcessorStartCommand, ProcessorStopCommand


class ManagerBase(IManager):
    def __init__(self, address: Address, scheduler: ITaskScheduler, processor: IProcessor, messenger: IMessenger):
        self._address = address
        self._scheduler = scheduler
        self._processor = processor
        self._messenger = messenger

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, ManagerSpawnActorMessage):
            self._processor.process(
                SpawnActorCommand(address=message.address, type_=message.type_, reply_to=sender, ref_id=message.ref_id))
        else:
            self._processor.process(MessageHandlingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, MessageHandlingCommand):
            self._handle_message(command)
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
            actor_address=command.address, manager_address=self._address, ref_id=command.ref_id
        )
        self._messenger.send(self._address, command.reply_to, reply_message)

    def _handle_message(self, command: MessageHandlingCommand):
        if command.receiver == self._address:
            self._handle_manager_message(command)
        else:
            self._scheduler.schedule(ActorMessageDeliveryTask(
                target=command.receiver,
                message=command.message,
                sender=command.sender,
            ))

    def _handle_manager_message(self, command: MessageHandlingCommand):
        if isinstance(command.message, SupervisorForceStop):
            self._scheduler.force_stop_actor(command.message.address)
