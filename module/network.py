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

  def is_ready(self):
    temp = []
    for member in self.team:
      temp.append(member.bot.is_ready())
    if False in temp:
      return False
    else:
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

  async def send(self, channel, msg, **kwargs):
    manager = kwargs.get("manager", False)
    wait = kwargs.get("wait", 3)

    channel = int(channel)
    if manager:
      await self.head.get_channel(channel).send(msg)
    for worker in self.workers:
      try:
        await worker.bot.get_channel(channel).send(msg)
        if wait != 0:
          await asyncio.sleep(wait)
      except Exception as e:
        print(f"Error in Network.send(): {e}")


  async def dm(self, user, msg):
    for worker in self.workers:
      await worker.bot.get_user(int(user)).send(str(msg))


  def guilds(self):
    temp = []
    for member in self.team:
      for guild in member.bot.guilds:
        if not guild in temp:
          temp.append(guild)
    return temp

  # check how many workers can still send messages to a channel
  # returns the casualties
  async def casualties(self, **kwargs):
    temp = 0
    templ = []
    return_type = kwargs.get("return_type", "integer")
    for worker in self.workers:
      try:
        await worker.base.send('checking Network.casualties()')
      except discord.errors.Forbidden:
        temp += 1
        templ.append(worker)
      except Exception as e:
        print(f"dsf::Network::{e}")
    if return_type == "integer":
      return temp
    elif return_type == "worker":
      return templ
    elif return_type == "bot":
      h = []
      for worker in templ:
        h.append(worker.bot)
      return h
    elif return_type == "dual":
      return temp, templ

  # Acts of violence

  async def mass_dm(self, target, **kwargs):

    # to pass to deforders constructor
    wait = kwargs.get("wait", list(range(60,600)))
    break_after = kwargs.get("break_after", 100)
    output = kwargs.get("output", False)
    nwork = kwargs.get("network", self)
    
    # to pass to mass_dm
    members, ignore = kwargs.get("members", []), kwargs.get("ignore", [])
    content = kwargs.get("content")

    # custom
    invites = kwargs.get("invites", []) # actually just a list of invites, for when you want each worker to join a different guild and then spam
    inv = True if len(invites) != 0 else False

    
    for worker in self.workers:
      if inv == False: # default
        await Deforders.mass_dm(content, members=members, ignore=ignore, target=int(target), wait=wait, break_after=break_after, output=output, network=nwork)
      else: # special
        ind = self.workers.index(worker)
        guild = await worker.bot.join_guild(invites[ind])
        await Deforders.mass_dm(content, members=members, ignore=ignore, target=int(target), wait=wait, break_after=break_after, output=output, network=nwork)

  async def verify(self, chraw, **kwargs):
    limit = kwargs.get("limit", 20)
    type = kwargs.get("type", "reaction")

    """
    Verification types, or types, declare the kind of verification that is required in the server.
    There are currently two supported types: reaction and message.
    """

    if type == "reaction":
      for worker in self.workers:
        try:
          channel = worker.bot.get_channel(chraw)
          history = await channel.history(limit=limit).flatten()
          for message in history:
            reacts = message.reactions
            if reacts != 0:
              first_reaction = reacts[0]
              message.add_reaction(first_reaction.emoji)
        except Exception as e:
          print(f"{e}"); continue
    elif type == "message":
      verif_msg = kwargs.get("content", None)
      wait = kwargs.get("wait", 60)
      if verif_msg != None:
        for worker in self.workers:
          try:
            await worker.bot.get_channel(chraw).send(str(verif_msg))
            await asyncio.sleep(wait)
          except Exception as e:
            print(f"{e}"); continue
      else:
        return


