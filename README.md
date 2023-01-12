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

```python
import time
from dataclasses import dataclass
from lyrid import ActorSystem, Actor, Address, Message, switch, use_switch


@dataclass
class TextMessage(Message):
    value: str


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
