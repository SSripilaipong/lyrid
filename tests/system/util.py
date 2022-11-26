from lyrid.base import ActorSystemBase
from lyrid.core.manager import ActorMessageSendingCommand
from lyrid.core.messaging import Address, Message


def root_process_message(system: ActorSystemBase, sender: Address, message: Message):
    system.handle_processor_command(ActorMessageSendingCommand(
        sender=sender, receiver=Address("$"), message=message,
    ))
