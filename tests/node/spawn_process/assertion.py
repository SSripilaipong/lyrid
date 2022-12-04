from lyrid.core.messaging import Address
from lyrid.core.node import NodeSpawnProcessMessage, SpawnProcessCommand, NodeSpawnProcessCompletedMessage
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.mock.scheduler import SchedulerMock
from tests.node.typing import NodeFactory
from ._actor_dummy import MyProcess
from ...message_dummy import MessageDummy


def assert_let_processor_process_spawn_process_command_when_handle_node_spawn_process_message(
        create_node: NodeFactory,
):
    processor = ProcessorMock()
    node = create_node(address=Address("#manager1"), processor=processor)

    node.handle_message(Address("$.me"), Address("#manager1"), NodeSpawnProcessMessage(
        address=Address("$.new"),
        type_=MyProcess,
        ref_id="RefId123",
        initial_message=MessageDummy("Hi!"),
    ))

    assert processor.process__command == SpawnProcessCommand(
        address=Address("$.new"), type_=MyProcess, initial_message=MessageDummy("Hi!"), reply_to=Address("$.me"),
        ref_id="RefId123",
    )


def assert_register_process_in_scheduler_when_handling_spawn_actor_command(
        create_node: NodeFactory,
):
    scheduler = SchedulerMock()
    messenger = MessengerMock()
    node = create_node(scheduler=scheduler, messenger=messenger)

    node.handle_processor_command(
        SpawnProcessCommand(address=Address("$.new"), type_=MyProcess, initial_message=MessageDummy("Hello!"),
                            reply_to=Address("$"), ref_id="RefId999"))

    assert scheduler.register_process__address == Address("$.new") and \
           scheduler.register_process__process == MyProcess(address=Address("$.new"), messenger=messenger) and \
           scheduler.register_process__initial_message == MessageDummy("Hello!")


def assert_reply_spawn_process_completed_message(
        create_node: NodeFactory,
):
    messenger = MessengerMock()
    node = create_node(address=Address("#manager1"), messenger=messenger)

    node.handle_processor_command(
        SpawnProcessCommand(address=Address("$.new"), type_=MyProcess, reply_to=Address("$"), ref_id="RefId999"))

    assert messenger.send__sender == Address("#manager1") and \
           messenger.send__receiver == Address("$") and \
           messenger.send__message == NodeSpawnProcessCompletedMessage(process_address=Address("$.new"),
                                                                       node_address=Address("#manager1"),
                                                                       ref_id="RefId999")
