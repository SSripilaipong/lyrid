import time
from dataclasses import dataclass
from typing import Optional, List

from lyrid import Address, Message, field, ActorSystem, StatefulActor, Ask, Reply


class Start(Message):
    pass


@dataclass
class Hello(Message):
    value: int


class GiveMeHelloList(Message):
    pass


@dataclass
class HelloList(Message):
    data: List[Hello]


class Greeter(StatefulActor):
    hello_list: List[Hello] = field(default_factory=list)
    reply_to: Optional[Address] = None
    ref_id: Optional[str] = None

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Start):
            self.tell(self.address, Hello(1), delay=0.01)
            self.tell(self.address, Hello(2))
        elif isinstance(message, Hello):
            self.hello_list.append(message)
        elif isinstance(message, Ask) and isinstance(message.message, GiveMeHelloList):
            self.reply_to = sender
            self.ref_id = message.ref_id

        if self.ref_id is not None and self.reply_to is not None and len(self.hello_list) == 2:
            self.tell(self.reply_to, Reply(HelloList(self.hello_list), ref_id=self.ref_id))


# noinspection DuplicatedCode
def test_should_get_hello_2_before_hello_1():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn("greeter", Greeter)
    time.sleep(0.05)
    system.tell(greeter, Start())
    time.sleep(0.05)
    result = system.ask(greeter, GiveMeHelloList())
    system.force_stop()
    assert result == HelloList([Hello(2), Hello(1)])
