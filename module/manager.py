# a layer
"""
this layer allows the normal bot instance to order workers
the order must be of a raw github page containing code to be executed
"""

class Manager:
  def __init__(self, base, **kwargs):
    self.listen = kwargs.get("listen")
    
    self.prefix = "!"
    self.base = base

    # instance made here can be used instance.bot
    self.bot = commands.Bot(command_prefix=self.prefix)

  async def prep(self):
    await self.bot.wait_until_ready()
    self.base = self.bot.get_channel(self.base)

  async def order(self, link):

    await self.base.send(str(link))
    # listens for messages
    # useful when you want stats
    # however, can slow down messaging to avoid getting caught by the API
    if self.listen:
      count = 0
      while True:
        msg = await self.bot.wait_for("message", check=lambda m: m.channel == base)
        count += 1
    
