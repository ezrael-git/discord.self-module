import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from github import Github

# contains all the code required to manage the network
# this is just a framework. to add more code, you can do so in index.py
class UserBot:

  def __init__(self, prefix: str, manager: int, creds: list):
    # prefix for the userbot
    self.prefix = prefix
    # teammates
    self.team = team
    # manager
    self.manager = manager
    # bot email, pass / token
    self.creds = creds
    # the bot instance made here can be interacted using instance.bot
    self.bot = commands.Bot(command_prefix=prefix)
    await self.bot.wait_until_ready()
 
  async def listen(self):
    while True:
      order = await self.bot.wait_for("message", check=lambda m: m.message.author.id == self.manager)
      eval str(order.content)

  def run(self):
    if len(self.creds) == 1:
      self.run(self.creds[0])
    else:
      self.run(self.creds[0], self.creds[1])





"""
example usage:
userbot = UserBot("!", 123, [])
userbot.listen()
userbot.run()
"""
