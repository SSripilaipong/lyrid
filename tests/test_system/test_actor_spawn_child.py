from lyrid import ActorBase
from lyrid.core.messaging import Address, Message
from lyrid.core.system import ActorSpawnChildActorMessage, ActorSpawnChildActorCommand
from tests.factory.system import create_actor_system
from tests.mock.processor import ProcessorMock


def test_should_let_processor_process_actor_spawn_child_actor_command_when_receive_actor_spawn_child_actor_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.handle_message(
        sender=Address("$.actor"),
        receiver=Address("$"),
        message=ActorSpawnChildActorMessage(key="my_child", type_=ChildActor)
    )

    assert processor.process__command == ActorSpawnChildActorCommand(
        actor_address=Address("$.actor"), child_key="my_child", child_type=ChildActor,
    )


class ChildActor(ActorBase):

    def receive(self, sender: Address, message: Message):
        pass
