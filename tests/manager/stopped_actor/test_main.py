from lyrid.core.actor import SupervisorForceStop
from lyrid.core.manager import MessageHandlingCommand
from lyrid.core.messaging import Address
from tests.factory.manager import create_manager
from tests.mock.scheduler import SchedulerMock


def test_should_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message():
    scheduler = SchedulerMock()
    manager = create_manager(address=Address("#manager1"), scheduler=scheduler)

    manager.handle_processor_command(MessageHandlingCommand(
        sender=Address("$.me"), receiver=Address("#manager1"),
        message=SupervisorForceStop(address=Address("$.me.my_child")),
    ))

    assert scheduler.force_stop_actor__address == Address("$.me.my_child")
