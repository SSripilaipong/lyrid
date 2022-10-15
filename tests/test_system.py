from lyrid.core.actor import IActor
from lyrid.core.messaging import Address, Message
from lyrid.core.messenger import IManager, IMessenger
from lyrid.core.system import ManagerSpawnActorMessage, SpawnActorCommand
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock
from tests.test_manager.assertion import assert_have_all_manager_behaviors


class MyActor(IActor):
    def receive(self, sender: Address, message: Message):
        pass

    @classmethod
    def create(cls, address: Address, messenger: IMessenger) -> IActor:
        pass


def test_should_be_a_manager():
    assert isinstance(create_actor_system(), IManager)


def test_should_have_behaviors_of_a_manager():
    assert_have_all_manager_behaviors(create_actor_system)


def test_should_send_spawn_actor_message_to_manager_via_messenger_when_handling_spawn_actor_processor_command():
    messenger = MessengerMock()
    system = create_actor_system(messenger=messenger, manager_addresses=[Address("#manager1")])

    system.handle_processor_command(SpawnActorCommand(key="hello", type_=MyActor))

    assert messenger.send__message == ManagerSpawnActorMessage(address=Address("$.hello"), type_=MyActor) and \
           messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1")


def test_should_let_processor_process_spawn_actor_command_when_spawn_is_called():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.spawn("hello", MyActor)

    assert processor.process__command == SpawnActorCommand(key="hello", type_=MyActor)
