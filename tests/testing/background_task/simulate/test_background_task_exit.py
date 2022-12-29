from lyrid import BackgroundTaskExited
from lyrid.testing import ActorTester
from tests.mock.actor import ActorMock


def test_should_let_actor_receive_background_task_exited_message_with_return_value():
    actor = ActorMock()
    tester = ActorTester(actor)

    tester.simulate.background_task_exit("TaskXXX")

    assert actor.on_receive__messages == [BackgroundTaskExited("TaskXXX", return_value=None, exception=None)] and \
           actor.on_receive__senders == [tester.actor_address]
