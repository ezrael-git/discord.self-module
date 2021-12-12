""" network.py
for the bundling of the manager and worker components
"""

class Network:
  def __init__(self, manager: list, workers: list):
    self.manager = manager[0]
    self.workers = workers
    self.head = self.manager.bot
    team = [self.manager]
    for i in self.workers: team.append(i)

  def _bots(self):
    temp = []
    for i in self.team: temp.append(i.bot)
    return temp

  def _sendable(self, clientuser):
    return self.head.get_user(clientuser.id)

  def wait_until_ready(self):
    for member in self.team:
      await member.bot.wait_until_ready()
    return True

  def join_guild(self, invite, **kwargs):
    wait = kwargs.get("wait", 60)
    for member in self.team:
      try:
        await member.bot.join_guild(invite)
        await asyncio.sleep(wait)
      except:
        continue
    return True

  def leave_guild(self, id, **kwargs):
    wait = kwargs.get("wait", 60)
    for member in self.team:
      try:
        await member.bot.leave_guild(id)
        await asyncio.sleep(wait)
      except:
        continue
    return True

  def listen_for(self, type):
    if type == "command":
      for member in self.workers:
        await member.hear()

  def disconnect(self, **kwargs):
    manager = kwargs.get("manager", False)
    for member in self.team:
      if member == self.manager:
        if manager == True:
          self.head.logout()
      else:
        member.bot.logout()
    return True
