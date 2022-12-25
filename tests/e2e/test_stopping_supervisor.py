import time
from dataclasses import dataclass
from typing import List, Optional

from lyrid import Actor, ActorSystem, Address, Message, Ask, ChildStopped


# noinspection DuplicatedCode
class Start(Message):
    pass


class Stop(Message):
    pass


@dataclass(frozen=True)
class IAmStopping(Message):
    address: Address


class Ping(Message):
    pass


class Pong(Message):
    pass


@dataclass
class GiveMeLog(Message):
    n: int


@dataclass
class Log(Message):
    records: List[Message]


class Child(Actor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, Ping):
            self.reply(sender, Pong(), ref_id=message.ref_id)

    def on_stop(self):
        self.tell(Address("$.logger"), IAmStopping(self.address))


class Parent(Actor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Start):
            self.spawn("child", Child())
        elif isinstance(message, Stop):
            self.stop()

    def on_stop(self):
        self.tell(Address("$.logger"), IAmStopping(self.address))


class Grandparent(Actor):
    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Start):
            self.spawn("parent", Parent(), initial_message=Start())
        elif isinstance(message, ChildStopped):
            self.tell(Address("$.logger"), message)


class Logger(Actor):
    def __init__(self):
        super().__init__()

        self._log: List[Message] = []
        self._n: Optional[int] = None
        self._ref_id: Optional[str] = None
        self._reply_to: Optional[Address] = None

    def on_receive(self, sender: Address, message: Message):
        if isinstance(message, Ask) and isinstance(message.message, GiveMeLog):
            self._n = message.message.n
            self._ref_id = message.ref_id
            self._reply_to = sender
        else:
            self._log.append(message)

        if self._reply_to is not None and len(self._log) == self._n:
            assert self._ref_id is not None
            self.reply(self._reply_to, Log(self._log), ref_id=self._ref_id)


def test_should_receive_all_stop_log():
    # noinspection DuplicatedCode
    system = ActorSystem(n_nodes=1)
    logger = system.spawn("logger", Logger())
    grandparent = system.spawn("grandparent", Grandparent(), initial_message=Start())
    time.sleep(0.008)
    parent = grandparent.child("parent")
    system.ask(parent.child("child"), Ping())

    system.tell(parent, Stop())

    log = system.ask(logger, GiveMeLog(n=3))
    system.force_stop()

    assert isinstance(log, Log) and set(log.records) == {ChildStopped(Address("$.grandparent.parent")),
                                                         IAmStopping(Address("$.grandparent.parent")),
                                                         IAmStopping(Address("$.grandparent.parent.child"))}
