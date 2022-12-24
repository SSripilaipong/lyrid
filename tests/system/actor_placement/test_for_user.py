from typing import Callable

from lyrid.base import ActorSystemBase
from lyrid.core.process import Process
from lyrid.core.system import SystemSpawnActorCommand
from tests.system.actor_placement.assertion import assert_handle_placement_like_when_spawning_child_process
from tests.system.process_dummy import ProcessDummy


def test_should_handle_placement_like_when_spawning_child_process():
    assert_handle_placement_like_when_spawning_child_process(spawn_process_with_factory(lambda: ProcessDummy()),
                                                             ProcessDummy)


def spawn_process_with_factory(factory: Callable[[], Process]):
    def spawn(system: ActorSystemBase):
        system.handle_processor_command(SystemSpawnActorCommand(key="my_child", process=factory()))

    return spawn
