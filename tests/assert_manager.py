from typing import Protocol

from lyrid.core.manager import ActorMessageDeliveryTask, ActorMessageSendingCommand, ITaskScheduler
from lyrid.core.messaging import Address
from lyrid.core.messenger import IManager
from lyrid.core.processor import ProcessorStartCommand, ProcessorStopCommand, IProcessor
from tests.message_dummy import MessageDummy
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


class ManagerFactory(Protocol):
    def __call__(self, *, processor: IProcessor = None, scheduler: ITaskScheduler = None) -> IManager: ...


def assert_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor(
        create_manager: ManagerFactory
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
        create_manager: ManagerFactory
):
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ProcessorStartCommand())

    assert scheduler.start__is_called


def assert_stop_task_scheduler_when_receive_processor_stop_command(
        create_manager: ManagerFactory
):
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ProcessorStopCommand())

    assert scheduler.stop__is_called


def assert_schedule_actor_task_when_handling_actor_message_sending_command(
        create_manager: ManagerFactory
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
