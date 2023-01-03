from lyrid import Actor, Address, Message
from lyrid.testing import ActorTester
from tests.message_dummy import MessageDummy
from tests.mock.actor import ActorMock


def test_should_return_active_actor():
    actor = ActorMock()
    tester = ActorTester(actor)

    assert tester.current_actor is actor


def test_should_return_new_actor_after_become():
    class MyActor(Actor):
        def on_receive(self, sender: Address, message: Message):
            self.become(ActorMock("new"))

    tester = ActorTester(MyActor())

    tester.simulate.tell(MessageDummy("do it"), by=Address("$"))

    assert tester.current_actor == ActorMock("new")
