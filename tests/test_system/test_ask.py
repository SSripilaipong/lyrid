from lyrid.core.messaging import Address
from lyrid.core.system import SystemAskCommand
from tests.factory.system import create_actor_system
from tests.message_dummy import MessageDummy
from tests.mock.id_generator import IdGeneratorMock
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
