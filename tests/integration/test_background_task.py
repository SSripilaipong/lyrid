import time
from dataclasses import dataclass, field
from typing import Optional, List

from lyrid import Address, Message, ActorSystem, BackgroundTaskExited, Ask, Actor, ActorProcess


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


class GiveMeReturnValueList(Message):
    pass


@dataclass
class ReturnValueList(Message):
    data: List


@dataclass
class Greeter(Actor):
    hello_list: List[Hello] = field(default_factory=list)
    hello_reply_to: Optional[Address] = None
    hello_ref_id: Optional[str] = None

    return_list: List = field(default_factory=list)
    return_reply_to: Optional[Address] = None
    return_ref_id: Optional[str] = None

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Start):
            self.run_in_background(self.delayed_hello, args=(1,))
            time.sleep(0.005)
            self.tell(self.address, Hello(2))
        elif isinstance(message, Hello):
            self.hello_list.append(message)
        elif isinstance(message, Ask) and isinstance(message.message, GiveMeHelloList):
            self.hello_reply_to = sender
            self.hello_ref_id = message.ref_id
        elif isinstance(message, BackgroundTaskExited):
            self.return_list.append(message.return_value)
        elif isinstance(message, Ask) and isinstance(message.message, GiveMeReturnValueList):
            self.return_reply_to = sender
            self.return_ref_id = message.ref_id

        if self.hello_ref_id is not None and self.hello_reply_to is not None and len(self.hello_list) == 2:
            self.reply(self.hello_reply_to, HelloList(self.hello_list), ref_id=self.hello_ref_id)
            # self.hello_reply_to = self.hello_ref_id = None  # comment this out to test ask reply with wrong ref id

        if self.return_ref_id is not None and self.return_reply_to is not None and len(self.return_list) == 1:
            self.reply(self.return_reply_to, ReturnValueList(self.return_list), ref_id=self.return_ref_id)
            self.return_reply_to = self.return_ref_id = None

    def delayed_hello(self, value: int):
        time.sleep(0.01)
        self.tell(self.address, Hello(value))
        return f"hello{value}"


# noinspection DuplicatedCode
def test_should_get_hello_2_before_hello_1():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn("greeter", ActorProcess(Greeter()))
    time.sleep(0.05)
    system.tell(greeter, Start())
    time.sleep(0.05)
    hello_result = system.ask(greeter, GiveMeHelloList())
    return_result = system.ask(greeter, GiveMeReturnValueList())
    system.force_stop()
    assert hello_result == HelloList([Hello(2), Hello(1)])
    assert return_result == ReturnValueList(["hello1"])
