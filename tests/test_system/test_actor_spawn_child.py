from lyrid import ActorBase
from lyrid.core.manager import ManagerSpawnActorMessage
from lyrid.core.messaging import Address, Message
from lyrid.core.system import ActorSpawnChildActorMessage, ActorSpawnChildActorCommand
from tests.factory.system import create_actor_system
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock


def test_should_let_processor_process_actor_spawn_child_actor_command_when_handling_actor_spawn_child_actor_message():
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


def test_should_send_manager_spawn_actor_message_to_manager_with_generated_ref_id():
    messenger = MessengerMock()
    id_gen = IdGeneratorMock(generate__return="GenId123")
    system = create_actor_system(address=Address("$"),
                                 messenger=messenger,
                                 manager_addresses=[Address("#manager1")],
                                 id_generator=id_gen)

    system.handle_processor_command(ActorSpawnChildActorCommand(
        actor_address=Address("$.actor"), child_key="my_child", child_type=ChildActor,
    ))

    assert messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1") and \
           messenger.send__message == \
           ManagerSpawnActorMessage(address=Address("$.actor.my_child"), type_=ChildActor, ref_id="GenId123")


class ChildActor(ActorBase):

    def receive(self, sender: Address, message: Message):
        pass
