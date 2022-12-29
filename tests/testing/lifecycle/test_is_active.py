from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_return_true_if_the_actor_is_active():
    tester = ActorTester(ActorMock())

    assert tester.is_running()
