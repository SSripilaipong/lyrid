from lyrid.base._command import ActorMessageSendingCommand
from lyrid.core.manager._task import ActorTask
from lyrid.core.messaging import Address
from tests.factory.manager import create_manager
from tests.message_dummy import MessageDummy
from tests.mock.scheduler import SchedulerMock


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
