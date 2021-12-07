# a layer
# allows for the normal discord-self bot instance to order 
# requires a team of properly configured workers


class Manager:
  def __init__(self, base):
    self.prefix = "!"
    self.base = base

    # instance made here can be used instance.bot
    self.bot = commands.Bot(command_prefix=self.prefix)

  async def prep():
    await self.bot.wait_until_ready()
    self.base = self.bot.get_channel(self.base)

  async def order(self, code, **kwargs):
    listen = kwargs.get("listen")
    
    await self.base.send(str(code))
    if listen:
      msg = await self.bot.wait_for("message", check=lambda m: m.channel == base)
      return msg
