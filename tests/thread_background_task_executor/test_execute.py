from dataclasses import dataclass

from lyrid import Address
from lyrid.core.background_task import BackgroundTaskExited
from tests.factory.thread_background_task_executor import create_thread_background_task_executor
from tests.mock.messenger import MessengerMock
from tests.mock.thread_client import ThreadClientMock


def test_should_start_thread_with_task_and_args():
    client = ThreadClientMock()
    executor = create_thread_background_task_executor(thread_client=client)

    def task(s, i):
        task.args = (s, i)

    task.args = None

    executor.execute("xxx", Address("$.me"), task, args=("a", 123))

    client.start_thread__function(*client.start_thread__args)

    assert task.args == ("a", 123)


def test_should_send_message_back_to_address_when_thread_completed():
    client = ThreadClientMock()
    messenger = MessengerMock()
    executor = create_thread_background_task_executor(thread_client=client, messenger=messenger)

    executor.execute("BgId123", Address("$.me"), lambda: None)
    messenger.send__clear_captures()

    client.start_thread__function(*client.start_thread__args)

    assert messenger.send__sender == messenger.send__receiver == Address("$.me") and \
           messenger.send__message == BackgroundTaskExited("BgId123")


def test_should_attach_return_value_in_background_task_exited_message():
    client = ThreadClientMock()
    messenger = MessengerMock()
    executor = create_thread_background_task_executor(thread_client=client, messenger=messenger)

    executor.execute("BgId456", Address("$.me"), lambda: 999)
    messenger.send__clear_captures()

    client.start_thread__function(*client.start_thread__args)

    assert messenger.send__message == BackgroundTaskExited("BgId456", return_value=999)


def test_should_attach_exception_if_raised():
    client = ThreadClientMock()
    messenger = MessengerMock()
    executor = create_thread_background_task_executor(thread_client=client, messenger=messenger)

    @dataclass
    class MyException(Exception):
        description: str

    def failing_task():
        raise MyException("abc")

    executor.execute("BgId456", Address("$.me"), failing_task)

    client.start_thread__function(*client.start_thread__args)

    assert messenger.send__message == BackgroundTaskExited("BgId456", exception=MyException("abc"))
