import time
from dataclasses import dataclass

from lyrid import Actor, Address, Message, ActorSystem, switch, use_switch


class WhoAreYou(Message):
    pass


@dataclass
class IAm(Message):
    name: str


class MakeHimAngry(Message):
    pass


class CalmDown(Message):
    pass


@dataclass
class Base(Actor):
    name: str

    @switch.ask(type=WhoAreYou)
    def who_are_you(self, sender: Address, ref_id: str):
        self.reply(sender, IAm(name=self.name), ref_id=ref_id)


@use_switch
@dataclass
class Banner(Base):

    @switch.message(type=MakeHimAngry)
    def make_him_angry(self):
        self.become(Hulk(name="Hulk"))


@use_switch
@dataclass
class Hulk(Base):

    @switch.message(type=CalmDown)
    def calm_down(self):
        self.become(Banner(name="Banner"))


def test_should_transit_state_back_and_forth():
    system = ActorSystem(n_nodes=1)

    try:
        banner = system.spawn(Banner(name="Banner"), key="banner")
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
