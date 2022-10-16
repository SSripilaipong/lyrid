from dataclasses import dataclass
from typing import TYPE_CHECKING

from lyrid.core.actor import IActor
from lyrid.core.manager import ManagerSpawnActorMessage, SpawnActorCommand, ManagerSpawnActorCompletedMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock
from tests.test_manager.typing import ManagerFactory


def assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message(
        create_manager: ManagerFactory,
):
    processor = ProcessorMock()
    manager = create_manager(address=Address("#manager1"), processor=processor)

    manager.handle_message(Address("$.me"), Address("#manager1"), ManagerSpawnActorMessage(
        address=Address("$.new"),
        type_=MyActor,
    ))

    assert processor.process__command == SpawnActorCommand(
        address=Address("$.new"), type_=MyActor, reply_to=Address("$.me"),
    )


def assert_register_actor_in_scheduler_when_handling_spawn_actor_command(
        create_manager: ManagerFactory,
):
    scheduler = SchedulerMock()
    messenger = MessengerMock()
    manager = create_manager(scheduler=scheduler, messenger=messenger)

    manager.handle_processor_command(SpawnActorCommand(address=Address("$.new"), type_=MyActor, reply_to=Address("$")))

    assert scheduler.register_actor__address == Address("$.new") and \
           scheduler.register_actor__actor == MyActor(address=Address("$.new"), messenger=messenger)


def assert_reply_spawn_actor_completed_message(
        create_manager: ManagerFactory,
):
    messenger = MessengerMock()
    manager = create_manager(address=Address("#manager1"), messenger=messenger)

    manager.handle_processor_command(SpawnActorCommand(address=Address("$.new"), type_=MyActor, reply_to=Address("$")))

    assert messenger.send__sender == Address("#manager1") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == ManagerSpawnActorCompletedMessage(actor_address=Address("$.new"),
                                                                        manager_address=Address("#manager1"))


@dataclass
class MyActor(IActor):
    address: Address
    messenger: IMessenger

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, address: Address, messenger: IMessenger): ...