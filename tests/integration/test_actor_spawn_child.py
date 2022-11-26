from dataclasses import dataclass
from typing import Optional

from lyrid import ActorBase, ActorSystem
from lyrid.core.actor import ActorStoppedSignal
from lyrid.core.messaging import Address, Message, Reply, Ask
from lyrid.core.messenger import IMessenger
from lyrid.core.system import SpawnChildCompletedMessage
from tests.message_dummy import MessageDummy


@dataclass
class GreetSecond(Message):
    pass


@dataclass
class SpawnSecond(Message):
    pass


class First(ActorBase):
    def __init__(self, address: Address, messenger: IMessenger):
        super().__init__(address, messenger)

        self.reply_to: Optional[Address] = None
        self.ref_id: Optional[str] = None
        self.second_address: Optional[Address] = None

    def receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, SpawnSecond):
            self.spawn("second", Second)
            self.tell(sender, Reply(MessageDummy("ok"), ref_id=message.ref_id))
        elif isinstance(message, Ask) and isinstance(message.message, GreetSecond):
            self.reply_to = sender
            self.ref_id = message.ref_id
            self._try_greet_second()
        elif isinstance(message, SpawnChildCompletedMessage):
            self.second_address = message.address
            self._try_greet_second()
        elif isinstance(message, MessageDummy) and sender == self.second_address:
            assert self.reply_to is not None and self.ref_id is not None
            self.tell(self.reply_to, Reply(MessageDummy("second said: " + message.text), ref_id=self.ref_id))
            raise ActorStoppedSignal()

    def _try_greet_second(self):
        if self.reply_to is None or self.second_address is None:
            return
        self.tell(self.second_address, MessageDummy("how are you"))


class Second(ActorBase):
    def receive(self, sender: Address, message: Message):
        if isinstance(message, MessageDummy) and message.text == "how are you":
            self.tell(sender, MessageDummy("i'm good, thanks"))
            raise ActorStoppedSignal()


def test_should_spawn_and_ask_second_actor():
    system = ActorSystem()
    first = system.spawn("first", First)

    system.ask(first, SpawnSecond())
    second_response = system.ask(first, GreetSecond())

    system.join()
    assert second_response == MessageDummy("second said: i'm good, thanks")
