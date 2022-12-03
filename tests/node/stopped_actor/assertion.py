from lyrid.core.messaging import Address
from lyrid.core.node import MessageHandlingCommand, ProcessNotFoundError
from lyrid.core.process import SupervisorForceStop, ChildStopped
from tests.mock.messenger import MessengerMock
from tests.mock.scheduler import SchedulerMock
from tests.node.typing import NodeFactory


def assert_force_stop_actor_on_scheduler_when_handling_supervisor_force_stop_message(
        create_manager: NodeFactory,
):
    scheduler = SchedulerMock()
    manager = create_manager(address=Address("#manager1"), scheduler=scheduler)

    manager.handle_processor_command(MessageHandlingCommand(
        sender=Address("$.me"), receiver=Address("#manager1"),
        message=SupervisorForceStop(address=Address("$.me.my_child")),
    ))

    assert scheduler.force_stop_actor__address == Address("$.me.my_child")


def assert_send_child_actor_stopped_message_when_scheduler_cannot_find_the_actor(
        create_manager: NodeFactory,
):
    messenger = MessengerMock()
    scheduler = SchedulerMock(force_stop_actor__raise=ProcessNotFoundError())
    manager = create_manager(address=Address("#manager1"), messenger=messenger, scheduler=scheduler)

    manager.handle_processor_command(MessageHandlingCommand(
        sender=Address("$.me"), receiver=Address("#manager1"),
        message=SupervisorForceStop(address=Address("$.me.my_child")),
    ))

    assert messenger.send__sender == Address("#manager1") and \
           messenger.send__receiver == Address("$.me") and \
           messenger.send__message == ChildStopped(child_address=Address("$.me.my_child"))