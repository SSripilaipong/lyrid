from dataclasses import dataclass

from lyrid import VanillaActor, Address, Message
from tests.factory.actor import create_actor
from tests.mock.background_task_executor import BackgroundTaskExecutorMock


@dataclass
class Start(Message):
    pass


class ActorWithBackgroundTask(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Start):
            self.run_in_background(self.do_something, args=("a", 123))

    def do_something(self, x, y):
        pass


def test_should_task_run_in_background_with_args():
    executor = BackgroundTaskExecutorMock()
    actor = create_actor(ActorWithBackgroundTask, background_task_executor=executor)

    actor.receive(Address("$.someone"), Start())

    assert executor.execute__task == actor.do_something and executor.execute__args == ("a", 123)
