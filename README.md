Lyrid
==============

[![PyPi Version](https://img.shields.io/pypi/v/lyrid)](https://pypi.org/project/lyrid/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/lyrid.svg)](https://pypi.org/project/lyrid/)
[![License](https://img.shields.io/github/license/ssripilaipong/lyrid)](https://github.com/SSripilaipong/lyrid/blob/master/LICENSE.md)

# Overview

An actor model framework that simplifies concurrent system while support real parallelism.
<br>

No thread/process/async/await, just actor. Implemented in pure Python.

<br>

[What is Actor Model?](https://github.com/SSripilaipong/lyrid/wiki/1.-What-is-Actor-Model)

# Requirements

- Python 3.8+
- Works on Linux, Windows, macOS, BSD

# Installation

using pip:

```
pip install lyrid
```

# Documentation

[What is Actor Model?](https://github.com/SSripilaipong/lyrid/wiki/1.-What-is-Actor-Model)

[Hello World in Lyrid](https://github.com/SSripilaipong/lyrid/wiki/2.-Hello-World)

[API Reference](https://github.com/SSripilaipong/lyrid/wiki/3.-API-Reference)

[GitHub Wiki](https://github.com/SSripilaipong/lyrid/wiki)

# Demo: Hello World Actor

Here is how we can build a simple actor that sends back text message "world" when receives text message "hello".

Please see [demo/hello_world/](./demo/hello_world) for the full script.

```python

...  # imports and message type definitions


@use_switch
class HelloWorld(Actor):

    # for when another actor send text message which is, actually, not used in this demo
    @switch.message(type=TextMessage)
    def receive_text_message(self, sender: Address, message: TextMessage):
        if message.value == "hello":
            self.tell(sender, TextMessage("world"))

    # for when user ask with text message
    @switch.ask(type=TextMessage)
    def receive_text_message_ask(self, sender: Address, message: TextMessage, ref_id: str):
        if message.value == "hello":
            self.reply(sender, TextMessage("world"), ref_id=ref_id)


if __name__ == "__main__":
    system = ActorSystem(n_nodes=1)
    my_actor = system.spawn(HelloWorld())
    time.sleep(1)
    print("response from actor:", system.ask(my_actor, TextMessage("hello")))
    system.force_stop()
```

`@switch.message()` is used for receiving message from other actors,
while `@switch.ask()` is used for receiving `Ask` message from user outside the system.

For more detail about this demo,
see [GitHub Wiki - Hello World](https://github.com/SSripilaipong/lyrid/wiki/2.-Hello-World).

# Demo: Simple Worker System - parallel computing for CPU-bounded tasks

Here is how we can build a simple worker system. Run this script, and monitor your CPU performance to see 4-5 of your
CPU cores running at ~100% for some time, **showing that Lyrid provides real parallelism.**

How this system works: 5 workers are spawned to nodes (with round-robin policy) to compute
some tasks. Then, the user outside the system feeds tasks to the workers. After each worker computed each task, it sends
the result to the result collector. The user outside the system waits for all the results to be collected

Please see [demo/simple_worker_system/](./demo/simple_worker_system) for the full script.

```python

...  # imports and message type definitions


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
```

**Caution** This style of pipeline might not be suit for processing big data in production, since it doesn't
handle [back-pressure](https://www.youtube.com/watch?v=I6eZ4ZyI1Zg) and doesn't prepare for failures.

# Demo: Background Task - run IO-bounded tasks concurrently

For IO-bounded tasks, like http request or read/write file, you might find `Actor.run_in_background()` useful, since it
runs the task in a new thread (from built-in `threading`) on the same process as the actor, meaning lower overhead.

The example below use only 1 actor called `IOWorker` to run multiple IO tasks at the same time. IO tasks are represented
by a function which runs `time.sleep()` and then return the assigned number of the task as a result back to the actor.
The actor gather all results and reply back to the user outside the system.

Please see [demo/background_task/](./demo/background_task) for the full script.

```python

...  # imports and message type definitions


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
```
