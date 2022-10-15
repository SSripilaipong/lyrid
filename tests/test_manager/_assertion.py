from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING

from lyrid.core.actor import IActor
from lyrid.core.manager import (
    ActorMessageDeliveryTask, ActorMessageSendingCommand, ITaskScheduler, SpawnActorCommand, ManagerSpawnActorMessage,
    ManagerSpawnActorCompletedMessage
)
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IManager, IMessenger
from lyrid.core.processor import ProcessorStartCommand, ProcessorStopCommand, IProcessor
from tests.message_dummy import MessageDummy
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


class ManagerFactory(Protocol):
    def __call__(self, *, address: Address = None, processor: IProcessor = None,
                 scheduler: ITaskScheduler = None, messenger: IMessenger = None) -> IManager: ...


def assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor(
        create_manager: ManagerFactory,
):
    processor = ProcessorMock()
    manager = create_manager(processor=processor)

    manager.handle_message(Address("$.me"), Address("$.you"), MessageDummy("Hello"))

    assert processor.process__command == ActorMessageSendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    )


def assert_start_task_scheduler_when_receive_processor_start_command(
        create_manager: ManagerFactory,
):
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ProcessorStartCommand())

    assert scheduler.start__is_called


def assert_stop_task_scheduler_when_receive_processor_stop_command(
        create_manager: ManagerFactory,
):
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ProcessorStopCommand())

    assert scheduler.stop__is_called


def assert_schedule_actor_task_when_handling_actor_message_sending_command(
        create_manager: ManagerFactory,
):
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ActorMessageSendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert scheduler.schedule__task == ActorMessageDeliveryTask(
        target=Address("$.you"),
        message=MessageDummy("Hello"),
        sender=Address("$.me"),
    )


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
