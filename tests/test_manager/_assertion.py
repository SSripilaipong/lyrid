from dataclasses import dataclass
from typing import TYPE_CHECKING

from lyrid.core.actor import IActor
from lyrid.core.manager import (
    ActorMessageDeliveryTask, ActorMessageSendingCommand
)
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IMessenger
from lyrid.core.processor import ProcessorStartCommand, ProcessorStopCommand
from tests.message_dummy import MessageDummy
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock
from tests.test_manager.typing import ManagerFactory


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


@dataclass
class MyActor(IActor):
    address: Address
    messenger: IMessenger

    def receive(self, sender: Address, message: Message):
        pass

    if TYPE_CHECKING:
        def __init__(self, address: Address, messenger: IMessenger): ...
