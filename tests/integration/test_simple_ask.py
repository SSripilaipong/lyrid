from dataclasses import dataclass

from lyrid import ActorSystem, ActorBase
from lyrid.core.actor import ActorStoppedSignal
from lyrid.core.messaging import Address, Message, Ask, Reply


@dataclass
class Greeting(Message):
    content: str


class Greeter(ActorBase):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Greeting):
            self.tell(sender, Reply(Greeting(content="Hi!"), ref_id=message.ref_id))
            raise ActorStoppedSignal()


def test_should_should_reply_ask():
    system = ActorSystem()
    greeter = system.spawn("greeter", Greeter)
    reply = system.ask(greeter, Greeting("Hello there"))
    system.force_stop()
    assert reply == Greeting("Hi!")
