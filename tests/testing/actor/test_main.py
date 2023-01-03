from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_return_active_actor():
    actor = ActorMock()
    tester = ActorTester(actor)

    assert tester.current_actor is actor
