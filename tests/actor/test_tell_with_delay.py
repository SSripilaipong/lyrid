from lyrid.core.messaging import Address
from tests.actor.actor_mock import MyActor
from tests.factory.actor import create_actor_process
from tests.message_dummy import MessageDummy
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.messenger import MessengerMock


def test_should_not_send_message_via_messenger_immediately():
    messenger = MessengerMock()
    executor = BackgroundTaskExecutorMock()

    actor = MyActor()
    _ = create_actor_process(actor, address=Address("$.me"), messenger=messenger,
                             background_task_executor=executor)

    actor.tell(Address("$.you"), MessageDummy("Hello!"), delay=555.123)

    assert messenger.send__sender is None and messenger.send__receiver is None and messenger.send__message is None


def test_should_execute_message_sending_in_background_executor():
    messenger = MessengerMock()
    executor = BackgroundTaskExecutorMock()

    actor = MyActor()
    _ = create_actor_process(actor, address=Address("$.from.me"), messenger=messenger,
                             background_task_executor=executor)

    actor.tell(Address("$.to.you"), MessageDummy("Yeah!"), delay=123)
    executor.execute_with_delay__task(*executor.execute_with_delay__args)

    assert messenger.send__sender == Address("$.from.me") and \
           messenger.send__receiver == Address("$.to.you") and \
           messenger.send__message == MessageDummy("Yeah!")


def test_should_execute_with_delay():
    executor = BackgroundTaskExecutorMock()

    actor = MyActor()
    _ = create_actor_process(actor, address=Address("$.from.me"), background_task_executor=executor)

    actor.tell(Address("$.to.you"), MessageDummy("Yeah!"), delay=123.456)

    assert executor.execute_with_delay__delay == 123.456
