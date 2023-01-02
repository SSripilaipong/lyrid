import time
from dataclasses import dataclass, field
from typing import Optional, List

from lyrid import Address, Message, ActorSystem, Actor, use_switch, switch


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


@use_switch
@dataclass
class Greeter(Actor):
    hello_list: List[Hello] = field(default_factory=list)
    hello_reply_to: Optional[Address] = None
    hello_ref_id: Optional[str] = None

    return_list: List = field(default_factory=list)
    return_reply_to: Optional[Address] = None
    return_ref_id: Optional[str] = None

    @switch.message(type=Start)
    def start(self):
        self.run_in_background(self.delayed_hello, args=(1,))
        time.sleep(0.005)
        self.tell(self.address, Hello(2))

    @switch.message(type=Hello)
    def hello(self, message: Hello):
        self.hello_list.append(message)

    @switch.ask(type=GiveMeHelloList)
    def ask_for_hello_list(self, sender: Address, ref_id: str):
        self.hello_reply_to = sender
        self.hello_ref_id = ref_id

    @switch.background_task_exited(exception=None)
    def background_task_exited(self, result: str):
        self.return_list.append(result)

    @switch.ask(type=GiveMeReturnValueList)
    def ask_for_return_value_list(self, sender: Address, ref_id: str):
        self.return_reply_to = sender
        self.return_ref_id = ref_id

    @switch.after_receive()
    def after_receive(self):
        if self.hello_ref_id is not None and self.hello_reply_to is not None and len(self.hello_list) == 2:
            self.reply(self.hello_reply_to, HelloList(self.hello_list), ref_id=self.hello_ref_id)
            # self.hello_reply_to = self.hello_ref_id = None  # comment this out to test ask reply with wrong ref id

        if self.return_ref_id is not None and self.return_reply_to is not None and len(self.return_list) == 1:
            self.reply(self.return_reply_to, ReturnValueList(self.return_list), ref_id=self.return_ref_id)
            self.return_reply_to = self.return_ref_id = None

    def delayed_hello(self, value: int):
        time.sleep(0.05)
        self.tell(self.address, Hello(value))
        return f"hello{value}"


# noinspection DuplicatedCode
def test_should_get_hello_2_before_hello_1():
    system = ActorSystem(n_nodes=1)
    greeter = system.spawn(Greeter(), key="greeter")
    time.sleep(0.05)
    system.tell(greeter, Start())
    time.sleep(0.05)
    hello_result = system.ask(greeter, GiveMeHelloList())
    return_result = system.ask(greeter, GiveMeReturnValueList())
    system.force_stop()
    assert hello_result == HelloList([Hello(2), Hello(1)])
    assert return_result == ReturnValueList(["hello1"])
