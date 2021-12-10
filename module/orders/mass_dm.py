target = worker.bot.get_channel(918533562033139804)
while True:
  worker.bot.loop.create_task(target.send("cum"))
  worker.bot.loop.create_task(self.base.send("sent"))
