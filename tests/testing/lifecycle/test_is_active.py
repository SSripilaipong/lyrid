from lyrid import Address
from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock, ActorMockStop


def test_should_return_true_if_the_actor_is_active():
    tester = ActorTester(ActorMock())

    assert tester.is_running()


def test_should_return_false_if_the_actor_is_stopped():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.tell(ActorMockStop(), by=Address("$"))

    assert not tester.is_running()
