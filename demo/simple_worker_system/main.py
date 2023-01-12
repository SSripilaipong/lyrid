import random
import time
from dataclasses import dataclass, field
from typing import List, Optional

from lyrid import ActorSystem, Message, Actor, use_switch, switch, Address, Placement, MatchType, RoundRobin


@dataclass
class StartGenerating(Message):
    n_problems: int


@dataclass
class AskForResults(Message):
    n_results: int


@dataclass
class Problem(Message):
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

    @switch.message(type=Problem)
    def receive_problem(self, message: Problem):
        expo = message.base ** message.expo
        self.tell(self.collector, Result(expo % message.mod))


@use_switch
@dataclass
class ProblemGenerator(Actor):
    workers: List[Address]

    @switch.message(type=StartGenerating)
    def start_generating(self, message: StartGenerating):
        for i in range(message.n_problems):
            worker = self.workers[i % len(self.workers)]

            self.tell(worker, Problem(base=random.randint(10, 99),
                                      expo=random.randint(100_000, 999_999),
                                      mod=random.randint(10, 10_000)))


if __name__ == "__main__":
    system = ActorSystem(n_nodes=7, placement=[Placement(MatchType(Worker), RoundRobin())])
    collector = system.spawn(ResultCollector(), key="collector")
    workers = [system.spawn(Worker(collector)) for _ in range(5)]
    problem_generator = system.spawn(ProblemGenerator(workers=workers))
    time.sleep(1)

    print("Starting")
    system.tell(problem_generator, StartGenerating(n_problems=5_00))
    results = system.ask(collector, AskForResults(n_results=5_00))
    system.force_stop()
    print(results)
