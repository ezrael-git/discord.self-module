worker.bot.loop.create_task(worker.bot.wait_until_ready())
target = worker.bot.get_channel(918533562033139804)
worker.bot.loop.create_task(target.send("cum"))
worker.bot.loop.create_task(self.base.send("sent"))
