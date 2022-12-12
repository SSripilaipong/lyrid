from lyrid import MatchAll
from tests.system.process_dummy import ProcessDummy


def test_should_always_return_true():
    assert MatchAll().match(ProcessDummy) is True
