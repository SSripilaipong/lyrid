from lyrid.core.messaging import Address
from lyrid.core.node import ProcessMessageDeliveryTask
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.process_mock import MyProcess


def test_should_let_process_do_scheduled_task():
    scheduler = create_scheduler()
    scheduler.start()

    process = MyProcess()
    scheduler.register_process(Address("$.you"), process)

    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.you"), MessageDummy("Hello"), Address("$.me")))

    scheduler.stop()

    assert process.receive__sender == Address("$.me") and \
           process.receive__message == MessageDummy("Hello")


def test_should_ignore_when_schedule_message_to_unknown_process():
    scheduler = create_scheduler()
    scheduler.start()

    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.who"), MessageDummy("Hello Stranger"), Address("$.me")))

    scheduler.stop()
