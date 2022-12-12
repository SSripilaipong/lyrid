from dataclasses import dataclass

from lyrid import VanillaActor, Address, Message
from tests.factory.actor import create_actor
from tests.mock.background_task_executor import BackgroundTaskExecutorMock
from tests.mock.id_generator import IdGeneratorMock


@dataclass
class RunSuccessTask(Message):
    pass


class ActorWithBackgroundTask(VanillaActor):

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, RunSuccessTask):
            self.run_in_background(self.success_task, args=("a", 123))

    def success_task(self, x, y):
        pass


def test_should_run_task_in_background_with_task_id_and_address_and_args():
    executor = BackgroundTaskExecutorMock()
    id_gen = IdGeneratorMock(generate__return="BgId456")
    actor = create_actor(ActorWithBackgroundTask, address=Address("$.me"), background_task_executor=executor,
                         id_gen=id_gen)

    actor.receive(Address("$.someone"), RunSuccessTask())

    assert executor.execute__address == Address("$.me") and \
           executor.execute__task_id == "BgId456" and \
           executor.execute__task == actor.success_task and \
           executor.execute__args == ("a", 123)


def test_should_return_generated_task_id():
    executor = BackgroundTaskExecutorMock()
    id_gen = IdGeneratorMock(generate__return="BgId123")
    actor = create_actor(ActorWithBackgroundTask, background_task_executor=executor, id_gen=id_gen)

    task_id = actor.run_in_background(actor.success_task, args=("x", 456))

    assert task_id == executor.execute__task_id == "BgId123"
