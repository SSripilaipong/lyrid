import time
from dataclasses import dataclass

from lyrid import ActorSystem, Actor, Address, Message, switch, use_switch


@dataclass
class TextMessage(Message):
    value: str


@use_switch
class HelloWorld(Actor):

    # for when another actor send text message which is, actually, not used in this demo
    @switch.message(type=TextMessage)
    def receive_text_message(self, sender: Address, message: TextMessage):
        if message.value == "hello":
            self.tell(sender, TextMessage("world"))

    # for when user ask with text message
    @switch.ask(type=TextMessage)
    def receive_text_message_ask(self, sender: Address, message: TextMessage, ref_id: str):
        if message.value == "hello":
            self.reply(sender, TextMessage("world"), ref_id=ref_id)


if __name__ == "__main__":
    system = ActorSystem(n_nodes=1)
    my_actor = system.spawn(HelloWorld())
    time.sleep(1)
    print("response from actor:", system.ask(my_actor, TextMessage("hello")))
    system.force_stop()
