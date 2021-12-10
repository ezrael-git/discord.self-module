"""
mass dms a channel
"""


async def cum():
  await worker.bot.wait_until_ready()
  target = worker.bot.get_channel(918533562033139804)
  while True:
    await target.send("cum")
    await asyncio.sleep(60)

worker.bot.loop.create_task(cum())
