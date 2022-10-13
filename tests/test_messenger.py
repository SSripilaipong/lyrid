from lyrid.core.messenger import Address
from lyrid.message import TextMessage
from tests.manager_mock import ManagerMock
from tests.messenger_factory import create_messenger_with_managers


def test_should_let_manager_of_the_registered_address_handle_the_message_on_sending():
    manager = ManagerMock()
    messenger = create_messenger_with_managers({
        "manager0": ManagerMock(),
        "manager1": manager,
        "manager2": ManagerMock(),
    })
    messenger.on_registering(Address("$.you"), "manager1")

    messenger.on_sending(Address("$.me"), Address("$.you"), TextMessage("Hello"))

    assert manager.handle_sender == Address("$.me") and \
           manager.handle_receiver == Address("$.you") and \
           manager.handle_message == TextMessage("Hello")
