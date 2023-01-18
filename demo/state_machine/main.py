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


if __name__ == "__main__":
    system = ActorSystem(n_nodes=1)

    actor = system.spawn(Banner(name="Banner"))
    print(system.ask(actor, WhoAreYou()))  # Output: IAm(name='Banner')

    system.tell(actor, MakeHimAngry())
    print(system.ask(actor, WhoAreYou()))  # Output: IAm(name='Hulk')

    system.tell(actor, CalmDown())
    print(system.ask(actor, WhoAreYou()))  # Output: IAm(name='Banner')

    system.force_stop()
