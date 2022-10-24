from lyrid.core.messaging import Address, Ask, Reply
from lyrid.core.system import SystemAskCommand, ActorReplyAskCommand
from tests.factory.system import create_actor_system
from tests.message_dummy import MessageDummy
from tests.mock.id_generator import IdGeneratorMock
from tests.mock.messenger import MessengerMock
from tests.mock.processor import ProcessorMock


def test_should_let_processor_process_system_ask_command_when_ask_is_called():
    processor = ProcessorMock()
    id_generator = IdGeneratorMock(generate__return="AskId123")
    system = create_actor_system(processor=processor, id_generator=id_generator)

    system.ask(Address("$.my_actor"), MessageDummy("Hello"))

    assert processor.process__command == SystemAskCommand(
        address=Address("$.my_actor"),
        message=MessageDummy("Hello"),
        ref_id="AskId123",
    )


def test_should_send_ask_message_via_messenger_when_handling_system_ask_command():
    messenger = MessengerMock()
    system = create_actor_system(address=Address("$"), messenger=messenger, manager_addresses=[Address("#manager1")])

    system.handle_processor_command(SystemAskCommand(
        address=Address("$.my_actor"),
        message=MessageDummy("Hello"),
        ref_id="AskId123",
    ))

    assert messenger.send__message == Ask(message=MessageDummy("Hello"), ref_id="AskId123") and \
           messenger.send__sender == Address("$") and \
           messenger.send__receiver == Address("$.my_actor")


def test_should_let_processor_process_actor_reply_ask_command_when_handling_reply_message():
    processor = ProcessorMock()
    system = create_actor_system(processor=processor)

    system.handle_message(
        sender=Address("$.my_actor"),
        receiver=Address("$"),
        message=Reply(message=MessageDummy("Hi"), ref_id="AskId123")
    )

    assert processor.process__command == ActorReplyAskCommand(
        address=Address("$.my_actor"),
        message=MessageDummy("Hi"),
        ref_id="AskId123",
    )
