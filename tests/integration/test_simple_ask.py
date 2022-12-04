from dataclasses import dataclass

from lyrid import ActorSystem, VanillaActor
from lyrid.core.messaging import Address, Message, Ask, Reply
from lyrid.core.process import ProcessStoppedSignal


@dataclass
class Greeting(Message):
    content: str


class Greeter(VanillaActor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Greeting):
            self.tell(sender, Reply(Greeting(content="Hi!"), ref_id=message.ref_id))
            raise ProcessStoppedSignal()


def test_should_should_reply_ask():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn("greeter", Greeter)
    reply = system.ask(greeter, Greeting("Hello there"))
    system.force_stop()
    assert reply == Greeting("Hi!")
