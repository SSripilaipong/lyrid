from lyrid.core.messaging import Address
from lyrid.core.node import ProcessMessageDeliveryTask
from tests.factory.scheduler import create_scheduler
from tests.message_dummy import MessageDummy
from tests.scheduler.process_mock import WillStop


def test_should_not_pass_message_to_process_after_process_stopped_signal_is_raised():
    scheduler = create_scheduler()
    scheduler.start()

    process = WillStop()
    scheduler.register_process(Address("$.you"), process)

    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.you"), MessageDummy("Hello1"), Address("$.sender1")))
    # the process already raised ProcessStoppedSignal
    scheduler.schedule(ProcessMessageDeliveryTask(Address("$.you"), MessageDummy("Hello2"), Address("$.sender2")))

    scheduler.stop()

    assert process.receive__senders == [Address("$.sender1")] and \
           process.receive__messages == [MessageDummy("Hello1")]
