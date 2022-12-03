from lyrid.core.messaging import Address
from lyrid.core.node import ProcessMessageDeliveryTask
from lyrid.core.process import WillForceStop
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.process_mock import MyProcess


def test_should_pass_will_force_stop_message_to_process():
    scheduler = create_scheduler()
    scheduler.start()

    process = MyProcess()
    scheduler.register_process(Address("$.you"), process)

    scheduler.force_stop_process(Address("$.you"))

    scheduler.stop()

    assert process.receive__sender == Address("$.you") and process.receive__message == WillForceStop()


def test_should_not_pass_message_to_process_after_process_is_forced_stopping():
    scheduler = create_scheduler()
    scheduler.start()

    process = MyProcess()
    scheduler.register_process(Address("$.you"), process)

    scheduler.force_stop_process(Address("$.you"))
    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.you"), MessageDummy("Hello2"), Address("$.sender2")))

    scheduler.stop()

    assert process.receive__senders == [Address("$.you")] and process.receive__messages == [WillForceStop()]
