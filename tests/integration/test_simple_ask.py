from dataclasses import dataclass

from lyrid import ActorSystem, VanillaActor, Address, Message, Ask


@dataclass
class Greeting(Message):
    content: str


class Greeter(VanillaActor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Greeting):
            self.reply(sender, Greeting(content="Hi!"), ref_id=message.ref_id)
            self.stop()


def test_should_should_reply_ask():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn("greeter", Greeter)
    reply = system.ask(greeter, Greeting("Hello there"))
    system.force_stop()
    assert reply == Greeting("Hi!")
