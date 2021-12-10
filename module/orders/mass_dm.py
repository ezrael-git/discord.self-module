"""
mass dms a channel
"""

worker.bot.loop.create_task(worker.bot.wait_until_ready())

target = worker.bot.get_channel(918533562033139804)

while True:
  worker.bot.loop.create_task(asyncio.sleep(60))
  worker.bot.loop.create_task(target.send("cum"))
