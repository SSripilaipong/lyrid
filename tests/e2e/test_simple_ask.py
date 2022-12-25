from dataclasses import dataclass

from lyrid import ActorSystem, Address, Message, Ask, Actor


@dataclass
class Greeting(Message):
    content: str


class Greeter(Actor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Greeting):
            self.reply(sender, Greeting(content="Hi!"), ref_id=message.ref_id)
            self.stop()


def test_should_should_reply_ask():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn(Greeter(), key="greeter")
    reply = system.ask(greeter, Greeting("Hello there"))
    system.force_stop()
    assert reply == Greeting("Hi!")
