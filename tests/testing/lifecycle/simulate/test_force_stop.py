from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_call_on_stop():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.force_stop()

    assert actor.on_stop__is_called
