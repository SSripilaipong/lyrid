import time
from dataclasses import dataclass

from lyrid import Actor, Address, Message, ActorSystem, switch, use_switch


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

    @switch.ask(type=WhoAreYou)
    def who_are_you(self, sender: Address, ref_id: str):
        self.reply(sender, IAm(self.__class__.__name__), ref_id=ref_id)


@use_switch
class Banner(Base):

    @switch.message(type=MakeHimAngry)
    def make_him_angry(self):
        self.become(Hulk())


@use_switch
class Hulk(Base):

    @switch.message(type=CalmDown)
    def calm_down(self):
        self.become(Banner())


def test_should_transit_state_back_and_forth():
    system = ActorSystem(n_nodes=1)

    try:
        banner = system.spawn(Banner(), key="banner")
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
