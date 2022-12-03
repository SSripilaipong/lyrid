from lyrid.base import ActorSystemBase
from lyrid.core.messaging import Address, Message
from lyrid.core.node import MessageHandlingCommand


def root_process_message(system: ActorSystemBase, sender: Address, message: Message):
    system.handle_processor_command(MessageHandlingCommand(
        sender=sender, receiver=Address("$"), message=message,
    ))
