from dataclasses import dataclass
from typing import Optional

from lyrid import ActorSystem, Address, Message, Actor, switch, use_switch
from tests.message_dummy import MessageDummy


@dataclass
class GreetSecond(Message):
    pass


@dataclass
class SpawnSecond(Message):
    pass


@use_switch
@dataclass
class First(Actor):
    reply_to: Optional[Address] = None
    ref_id: Optional[str] = None
    second_address: Optional[Address] = None

    @switch.message(type=SpawnSecond)
    def spawn_second(self):
        self.spawn(Second())

    @switch.ask(type=GreetSecond)
    def greet_second(self, sender: Address, ref_id: str):
        self.reply_to = sender
        self.ref_id = ref_id
        self._try_greet_second()

    @switch.child_spawned()
    def child_spawned(self, address: Address):
        self.second_address = address
        self._try_greet_second()

    @switch.message(type=MessageDummy)
    def receive_message(self, message: MessageDummy):
        assert self.reply_to is not None and self.ref_id is not None
        self.reply(self.reply_to, MessageDummy("second said: " + message.text), ref_id=self.ref_id)
        self.stop()

    def _try_greet_second(self):
        if self.reply_to is None or self.second_address is None:
            return
        self.tell(self.second_address, MessageDummy("how are you"))


@use_switch
class Second(Actor):
    @switch.message(type=MessageDummy)
    def receive_message(self, sender: Address, message: MessageDummy):
        assert message.text == "how are you"
        self.tell(sender, MessageDummy("i'm good, thanks"))
        self.stop()


def test_should_spawn_and_ask_second_actor():
    system = ActorSystem(n_nodes=1)
    first = system.spawn(First(), initial_message=SpawnSecond())

    second_response = system.ask(first, GreetSecond())

    system.force_stop()
    assert second_response == MessageDummy("second said: i'm good, thanks")
