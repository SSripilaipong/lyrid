from lyrid.core.messaging import Address
from lyrid.core.node import NodeSpawnProcessMessage, SpawnProcessCommand, NodeSpawnProcessCompletedMessage
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock
from tests.node.typing import NodeFactory
from ._actor_dummy import MyProcess


def assert_let_processor_process_spawn_actor_command_when_handle_manager_spawn_actor_message(
        create_manager: NodeFactory,
):
    processor = ProcessorMock()
    manager = create_manager(address=Address("#manager1"), processor=processor)

    manager.handle_message(Address("$.me"), Address("#manager1"), NodeSpawnProcessMessage(
        address=Address("$.new"),
        type_=MyProcess,
        ref_id="RefId123",
    ))

    assert processor.process__command == SpawnProcessCommand(
        address=Address("$.new"), type_=MyProcess, reply_to=Address("$.me"), ref_id="RefId123",
    )


def assert_register_actor_in_scheduler_when_handling_spawn_actor_command(
        create_manager: NodeFactory,
):
    scheduler = SchedulerMock()
    messenger = MessengerMock()
    manager = create_manager(scheduler=scheduler, messenger=messenger)

    manager.handle_processor_command(
        SpawnProcessCommand(address=Address("$.new"), type_=MyProcess, reply_to=Address("$"), ref_id="RefId999"))

    assert scheduler.register_process__address == Address("$.new") and \
           scheduler.register_process__process == MyProcess(address=Address("$.new"), messenger=messenger)


def assert_reply_spawn_actor_completed_message(
        create_manager: NodeFactory,
):
    messenger = MessengerMock()
    manager = create_manager(address=Address("#manager1"), messenger=messenger)

    manager.handle_processor_command(
        SpawnProcessCommand(address=Address("$.new"), type_=MyProcess, reply_to=Address("$"), ref_id="RefId999"))

    assert messenger.send__sender == Address("#manager1") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == NodeSpawnProcessCompletedMessage(actor_address=Address("$.new"),
                                                                       manager_address=Address("#manager1"),
                                                                       ref_id="RefId999")
