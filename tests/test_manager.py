from lyrid.core.manager import ActorTask, ActorMessageSendingCommand
from lyrid.core.messaging import Address
from tests.factory.manager import create_manager
from tests.message_dummy import MessageDummy
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock


def test_should_let_processor_process_actor_message_sending_command_when_handle_message_with_address_of_a_registered_actor():
    processor = ProcessorMock()
    manager = create_manager(processor=processor)

    manager.handle_message(Address("$.me"), Address("$.you"), MessageDummy("Hello"))

    assert processor.process__command == ActorMessageSendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    )


def test_should_schedule_actor_task_when_handling_actor_message_sending_command():
    scheduler = SchedulerMock()
    manager = create_manager(scheduler=scheduler)

    manager.handle_processor_command(ActorMessageSendingCommand(
        sender=Address("$.me"),
        receiver=Address("$.you"),
        message=MessageDummy("Hello"),
    ))

    assert scheduler.schedule__task == ActorTask(
        target=Address("$.you"),
        message=MessageDummy("Hello"),
        sender=Address("$.me"),
    )
