from lyrid.core.messaging import Address
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.process_mock import MyProcess


def test_should_let_process_handle_initial_message_if_not_none():
    scheduler = create_scheduler()
    scheduler.start()

    process = MyProcess()
    scheduler.register_process(Address("$.supervisor.you"), process, initial_message=MessageDummy("Start!"))

    scheduler.stop()

    assert process.receive__sender == Address("$.supervisor") and \
           process.receive__message == MessageDummy("Start!")
