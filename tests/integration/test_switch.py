from dataclasses import dataclass

from lyrid import StatefulActor, Switch, Message, Address, ActorSystem


@dataclass
class IncreaseN(Message):
    by: int


@dataclass
class DecreaseN(Message):
    by: int


@dataclass
class GetN(Message):
    pass


@dataclass
class NValue(Message):
    n: int


class MyActor(StatefulActor):
    n: int = 0

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=IncreaseN)
    def increase_n(self, message: IncreaseN):
        self.n += message.by

    @switch.message(type=DecreaseN)
    def decrease_n(self, message: DecreaseN):
        self.n -= message.by

    @switch.ask(type=GetN)
    def get_n(self, sender: Address, _: GetN, ref_id: str):
        self.reply(sender, NValue(self.n), ref_id=ref_id)


def test_main():
    system = ActorSystem()
    my_actor = system.spawn("my_actor", MyActor)

    try:
        assert system.ask(my_actor, GetN()) == NValue(0)

        system.tell(my_actor, IncreaseN(by=9))
        assert system.ask(my_actor, GetN()) == NValue(9)

        system.tell(my_actor, DecreaseN(by=3))
        assert system.ask(my_actor, GetN()) == NValue(6)
    finally:
        system.force_stop()
