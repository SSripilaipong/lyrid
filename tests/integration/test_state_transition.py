import time
from dataclasses import dataclass

from lyrid import Actor, Address, Message, Ask, ActorSystem, ActorProcess


class WhoAreYou(Message):
    pass


@dataclass
class IAm(Message):
    type_: str


class MakeHimAngry(Message):
    pass


class CalmDown(Message):
    pass


class Base(Actor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, WhoAreYou):
            self.reply(sender, IAm(self.__class__.__name__), ref_id=message.ref_id)


class Banner(Base):
    def on_receive(self, sender: Address, message: Message):
        super().on_receive(sender, message)

        if isinstance(message, MakeHimAngry):
            self.become(Hulk())


class Hulk(Base):
    def on_receive(self, sender: Address, message: Message):
        super().on_receive(sender, message)

        if isinstance(message, CalmDown):
            self.become(Banner())


def test_should_transit_state_back_and_forth():
    system = ActorSystem(n_nodes=1)

    try:
        banner = system.spawn("banner", ActorProcess(Banner()))
        time.sleep(0.03)

        assert system.ask(banner, WhoAreYou()) == IAm('Banner')

        system.tell(banner, MakeHimAngry())
        time.sleep(0.03)
        assert system.ask(banner, WhoAreYou()) == IAm('Hulk')

        system.tell(banner, CalmDown())
        time.sleep(0.03)
        assert system.ask(banner, WhoAreYou()) == IAm('Banner')

        system.tell(banner, MakeHimAngry())
        time.sleep(0.03)
        assert system.ask(banner, WhoAreYou()) == IAm('Hulk')

    finally:
        system.force_stop()
