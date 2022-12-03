from lyrid.core.command_processing_loop import Command, CommandProcessingLoop, ProcessorStartCommand, \
    ProcessorStopCommand
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger, Node
from lyrid.core.node import (
    TaskScheduler, ProcessMessageDeliveryTask, MessageHandlingCommand, SpawnProcessCommand, NodeSpawnProcessMessage,
    NodeSpawnProcessCompletedMessage, ProcessNotFoundError,
)
from lyrid.core.process import SupervisorForceStop, ChildStopped


class ProcessManagingNode(Node):
    def __init__(self, address: Address, scheduler: TaskScheduler, processor: CommandProcessingLoop,
                 messenger: IMessenger):
        self._address = address
        self._scheduler = scheduler
        self._processor = processor
        self._messenger = messenger

    def handle_message(self, sender: Address, receiver: Address, message: Message):
        if isinstance(message, NodeSpawnProcessMessage):
            self._processor.process(
                SpawnProcessCommand(address=message.address, type_=message.type_, reply_to=sender,
                                    ref_id=message.ref_id))
        else:
            self._processor.process(MessageHandlingCommand(sender=sender, receiver=receiver, message=message))

    def handle_processor_command(self, command: Command):
        if isinstance(command, MessageHandlingCommand):
            self._handle_message(command)
        elif isinstance(command, ProcessorStartCommand):
            self._scheduler.start()
        elif isinstance(command, ProcessorStopCommand):
            self._scheduler.stop()
        elif isinstance(command, SpawnProcessCommand):
            self._spawn_actor(command)
        else:
            raise NotImplementedError()

    def _spawn_actor(self, command: SpawnProcessCommand):
        self._scheduler.register_process(command.address, command.type_(command.address, self._messenger))
        reply_message = NodeSpawnProcessCompletedMessage(
            actor_address=command.address, manager_address=self._address, ref_id=command.ref_id
        )
        self._messenger.send(self._address, command.reply_to, reply_message)

    def _handle_message(self, command: MessageHandlingCommand):
        if command.receiver == self._address:
            self._handle_manager_message(command)
        else:
            self._scheduler.schedule(ProcessMessageDeliveryTask(
                target=command.receiver,
                message=command.message,
                sender=command.sender,
            ))

    def _handle_manager_message(self, command: MessageHandlingCommand):
        if isinstance(command.message, SupervisorForceStop):
            try:
                self._scheduler.force_stop_process(command.message.address)
            except ProcessNotFoundError:
                self._messenger.send(
                    sender=self._address, receiver=command.sender,
                    message=ChildStopped(child_address=command.message.address),
                )