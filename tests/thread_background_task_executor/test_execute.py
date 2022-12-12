from lyrid import Address
from tests.factory.thread_background_task_executor import create_thread_background_task_executor
from tests.mock.thread_client import ThreadClientMock


def test_should_start_thread_with_task_and_args():
    client = ThreadClientMock()
    executor = create_thread_background_task_executor(thread_client=client)

    def task(s, i):
        task.args = (s, i)

    task.args = None

    executor.execute(Address("$.me"), task, args=("a", 123))

    client.start_thread__function(*client.start_thread__args)

    assert task.args == ("a", 123)
