import random
import string
import time
from dataclasses import dataclass, field
from typing import Optional, List

from lyrid import Switch, Message, Address, ActorSystem, Placement, MatchAll, RoundRobin, Actor, ActorProcess


@dataclass
class Ping(Message):
    payload: str = ""


@dataclass
class Pong(Message):
    payload: str = ""


# noinspection SpellCheckingInspection
@dataclass
class Start(Message):
    ponger: Address
    count: int
    message_size: int


class GetResult(Message):
    pass


@dataclass
class Result(Message):
    data: List[float]


# noinspection SpellCheckingInspection
class Ponger(Actor):
    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=Ping)
    def pinged(self, sender: Address, message: Ping):
        self.tell(sender, Pong(payload=message.payload))


# noinspection SpellCheckingInspection
@dataclass
class Pinger(Actor):
    timestamp: float = .0
    ponger: Optional[Address] = None
    result: List[float] = field(default_factory=list)
    count: int = 0
    message_size: int = 0

    user: Optional[Address] = None
    user_ref: Optional[str] = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=Start)
    def start(self, message: Start):
        self.ponger = message.ponger
        self.count = message.count
        self.message_size = message.message_size
        self.ping()

    @switch.message(type=Pong)
    def ponged(self):
        self.result.append(time.perf_counter() - self.timestamp)
        self.count -= 1
        if self.count > 0:
            self.ping()

        self.reply_if_possible()

    @switch.ask(type=GetResult)
    def asked_for_result(self, sender: Address, ref_id: str):
        self.user = sender
        self.user_ref = ref_id
        self.reply_if_possible()

    def ping(self):
        msg = Ping(payload=''.join(random.choice(string.ascii_lowercase) for _ in range(self.message_size)))
        self.timestamp = time.perf_counter()
        self.tell(self.ponger, msg)

    def reply_if_possible(self):
        if self.user is not None and self.count <= 0:
            self.reply(self.user, Result(self.result), ref_id=self.user_ref)


# noinspection SpellCheckingInspection
def main():
    n_loop, message_size = 1_000, 10_000

    s = ActorSystem(n_nodes=3, placement=[Placement(MatchAll(), RoundRobin())])
    ponger = s.spawn("ponger", ActorProcess(Ponger()))
    time.sleep(0.1)
    pinger = s.spawn("pinger", ActorProcess(Pinger()), initial_message=Start(ponger, n_loop, message_size))
    time.sleep(0.1)

    result = s.ask(pinger, GetResult())
    s.force_stop()
    assert isinstance(result, Result)
    r = [x * 1_000 for x in result.data]
    print(f"message size: {message_size:,} characters; #loops: {n_loop}")
    print(f'min: {min(r):.2f}ms, avg: {sum(r) / n_loop:.2f}ms, max: {max(r):.2f}ms')


if __name__ == '__main__':
    main()
