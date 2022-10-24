from dataclasses import dataclass

from lyrid import ActorSystem, ActorBase
from lyrid.core.actor import ActorStoppedSignal
from lyrid.core.messaging import Address, Message, Ask, Reply


@dataclass
class Greeting(Message):
    content: str


class Greeter(ActorBase):
    def receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Greeting):
            self.tell(sender, Reply(Greeting(content="Hi!"), ref_id=message.ref_id))
            raise ActorStoppedSignal()


def _test_should_should_reply_ask():
    system = ActorSystem()
    greeter = system.spawn("greeter", Greeter)
    print("spawned", greeter)
    reply = system.ask(greeter, Greeting("Hello there"))
    print("replied", reply)

    assert reply == Greeting("Hi!")
