from lyrid import MatchAll
from tests.system.process_dummy import ProcessDummyWithContext


def test_should_always_return_true():
    assert MatchAll().match(ProcessDummyWithContext) is True
