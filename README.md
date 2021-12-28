# discord.self.framework
An efficient framework to interact with a network of discord users instead of bots.
Includes network member code, manager code and more.
Designed to be as efficient as possible.


# Getting Started
1) download module/core.py
2) read examples/example.py

The core.py file serves as a "do-everything" file so you don't have to install anything else (other than dependencies, of course).
This will change in the future.

Docs: in the code



# Dependencies
- discord.py-self == 1.9.1
- Flask == 2.0.2
- requests == 2.26.0
- PyGithub == 1.55
- asyncio == 3.4.3

# Usage
```python
from core import dsf
base_channel = 123
manager_id = 123

dsf.filetype("dual")

network = Network(
    [
      Manager(base_channel)
    ], 
    [
      Worker(manager_id, base_channel),
      Worker(manager_id, base_channel)
    ]
  )

network.send(123, "hello")

network.connect(
    [
      "123",
      "456"
    ]
  )
```
