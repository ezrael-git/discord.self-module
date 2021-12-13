""" network.py
for the bundling of the manager and worker components
"""
import time

class Network:
  def __init__(self, manager: list, workers: list):
    self.manager = manager[0]
    self.workers = workers
    self.head = self.manager.bot
    self.team = [self.manager]
    for i in self.workers: self.team.append(i)

  def _bots(self):
    temp = []
    for i in self.team: temp.append(i.bot)
    return temp

  def _sendable(self, clientuser):
    return self.head.get_user(clientuser.id)

  async def _thread(self, loop):
    loop.run_forever()

  def connect(self, tokens: list, **kwargs):
    output = kwargs.get("output", False)
    wait = kwargs.get("wait", 5)
    additional = kwargs.get("additional", {})

    if output == True: print(f"Network.connect(): initiated")

    loop = asyncio.get_event_loop()
    for member,token in zip(self.team,tokens):
      loop.create_task(member.bot.start(token))
      if output == True: print(f"Network.connect(): {member} has been added to the loop")
      time.sleep(wait)

    # resolving additional
    if len(additional) != 0:
      count = 0
      for add in additional.items():
        count += 1
        _bot, _token = add[0], add[1]

        print(_bot)
        print(_token)

        loop.create_task(_bot.start(str(_token)))
        if output == True: print(f"Network.connect(): resolved add {count} of {len(additional)}")
      time.sleep(wait)

    if output == True: print(f"Network.connect(): resolved")
    loop.run_forever()


  def disconnect(self, **kwargs):
    manager = kwargs.get("manager", False)
    for member in self.team:
      if member == self.manager:
        if manager == True:
          self.head.logout()
      else:
        member.bot.logout()
    return True
    

  async def wait_until_ready(self):
    for member in self.team:
      await member.bot.wait_until_ready()
    return True

  async def join_guild(self, invite, **kwargs):
    wait = kwargs.get("wait", 60)
    for member in self.team:
      try:
        await member.bot.join_guild(invite)
        await asyncio.sleep(wait)
      except:
        continue
    return True

  async def leave_guild(self, id, **kwargs):
    wait = kwargs.get("wait", 60)
    for member in self.team:
      try:
        await member.bot.leave_guild(id)
        await asyncio.sleep(wait)
      except:
        continue
    return True

  async def listen_for(self, type):
    if type == "command":
      for member in self.workers:
        await member.hear()


