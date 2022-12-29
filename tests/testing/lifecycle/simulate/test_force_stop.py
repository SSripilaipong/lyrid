from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_call_on_stop():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.force_stop()

    assert actor.on_stop__is_called


def test_should_suppress_any_exception():
    tester = ActorTester(ActorMock(on_stop__raise=MyError()))

    tester.simulate.force_stop()


class MyError(Exception):
    pass
