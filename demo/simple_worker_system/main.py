import random
import time
from dataclasses import dataclass, field
from typing import List, Optional

from lyrid import ActorSystem, Message, Actor, use_switch, switch, Address, Placement, RoundRobin, MatchAll


@dataclass
class AskForResults(Message):
    n_results: int


@dataclass
class Task(Message):
    base: int
    expo: int
    mod: int


@dataclass
class Result(Message):
    value: int


@dataclass
class Results(Message):
    values: List[int]


@use_switch
@dataclass
class ResultCollector(Actor):
    results: List[int] = field(default_factory=list)

    user_address: Optional[Address] = None
    user_ref_id: Optional[str] = None
    expected_n_results: Optional[int] = None

    @switch.message(type=Result)
    def receive_data(self, message: Result):
        self.results.append(message.value)

    @switch.ask(type=AskForResults)
    def user_ask_for_result(self, sender: Address, ref_id: str, message: AskForResults):
        self.user_address = sender
        self.user_ref_id = ref_id
        self.expected_n_results = message.n_results

    @switch.after_receive()
    def after_receive(self):
        if None in (self.user_ref_id, self.user_address, self.expected_n_results):
            return

        if self.expected_n_results <= len(self.results):
            self.reply(self.user_address, Results(self.results), ref_id=self.user_ref_id)


@use_switch
@dataclass
class Worker(Actor):
    collector: Address

    @switch.message(type=Task)
    def receive_task(self, message: Task):
        expo = message.base ** message.expo
        self.tell(self.collector, Result(expo % message.mod))


if __name__ == "__main__":
    system = ActorSystem(n_nodes=7, placement=[Placement(MatchAll(), RoundRobin())])
    collector = system.spawn(ResultCollector())
    workers = [system.spawn(Worker(collector)) for _ in range(5)]
    time.sleep(1)

    print("Starting")
    for i in range(300):
        worker = workers[i % len(workers)]
        system.tell(worker, Task(base=random.randint(10, 99),
                                 expo=random.randint(100_000, 999_999),
                                 mod=random.randint(10, 10_000)))

    results = system.ask(collector, AskForResults(n_results=300))
    system.force_stop()
    print(results)
