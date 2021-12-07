# a layer
# makes the normal discord-self bot instance able to work in a network

class UserBot:

  def __init__(self, manager: int):
    # prefix for the userbot
    self.prefix = "!"

    # teammates
    self.team = team

    # manager
    self.manager = manager

    # the bot instance made here can be interacted using instance.bot
    self.bot = commands.Bot(command_prefix=prefix)
    await self.bot.wait_until_ready()
 
  async def listen(self):
    while True:
      order = await self.bot.wait_for("message", check=lambda m: m.message.author.id == self.manager)
      eval str(order.content)
