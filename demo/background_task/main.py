import time
from dataclasses import dataclass, field
from typing import List, Optional

from lyrid import Actor, use_switch, switch, Message, Address, ActorSystem


@dataclass
class RunTasks(Message):
    n_tasks: int


@dataclass
class Results(Message):
    values: List[int]


def io_task(number: int, sleep_time: int) -> int:
    time.sleep(sleep_time / 2)
    return number


@use_switch
@dataclass
class IOWorker(Actor):
    results: List[int] = field(default_factory=list)

    user_address: Optional[Address] = None
    user_ref_id: Optional[str] = None
    expected_n_results: Optional[int] = None

    @switch.ask(type=RunTasks)
    def receive_run_tasks(self, message: RunTasks, sender: Address, ref_id: str):
        n = message.n_tasks
        for i in range(n):
            self.run_in_background(io_task, args=(i, n - i,))

        self.user_address = sender
        self.user_ref_id = ref_id
        self.expected_n_results = n

    @switch.background_task_exited(exception=None)
    def background_task_completed(self, result: int):
        self.results.append(result)

    @switch.after_receive()
    def after_receive(self):
        if self.expected_n_results <= len(self.results):
            self.reply(self.user_address, Results(self.results), ref_id=self.user_ref_id)


if __name__ == "__main__":
    system = ActorSystem(n_nodes=1)
    worker = system.spawn(IOWorker())
    time.sleep(1)

    results = system.ask(worker, RunTasks(n_tasks=5))
    system.force_stop()
    print(results)  # Output: Results(values=[4, 3, 2, 1, 0]); reversed order since they are all executed in background
