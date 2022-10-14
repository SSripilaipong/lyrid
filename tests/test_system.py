from lyrid.core.actor import IActor
from lyrid.core.messaging import Address, Message
from lyrid.core.system import ManagerSpawnActorCommand
from tests.factory.system import create_actor_system
from tests.mock.messenger import MessengerMock


class MyActor(IActor):
    def receive(self, sender: Address, message: Message):
        pass


def test_should_send_spawn_actor_message_to_manager_via_messenger():
    messenger = MessengerMock()
    system = create_actor_system(messenger=messenger, manager_addresses=[Address("#manager1")])

    system.spawn("hello", MyActor)

    assert messenger.send__message == ManagerSpawnActorCommand(address=Address("$.hello"), type_=MyActor) and \
           messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("#manager1")
