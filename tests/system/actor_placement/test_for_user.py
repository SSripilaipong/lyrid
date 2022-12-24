from lyrid.base import ActorSystemBase
from lyrid.core.process import ProcessFactory
from lyrid.core.system import SystemSpawnActorCommand
from tests.system.actor_placement.assertion import assert_handle_placement_like_when_spawning_child_process
from tests.system.process_dummy import ProcessDummyWithContext


def test_should_handle_placement_like_when_spawning_child_process():
    assert_handle_placement_like_when_spawning_child_process(spawn_process_with_type(ProcessDummyWithContext),
                                                             ProcessDummyWithContext)


def spawn_process_with_type(type_: ProcessFactory):
    def spawn(system: ActorSystemBase):
        system.handle_processor_command(SystemSpawnActorCommand(key="my_child", type_=type_))

    return spawn
