# deforder.py

# contains all the default orders, also called deforders
# deforders are executed directly, there is no need to worker.hear()



class Deforders:
  """
  Method arguments and their meanings
  Args:
    target (discord.etc) : the channel or guild that should be targeted

  Kwargs:
    wait (list, [60-600]) : a list containing the number of seconds that should be waited for, the definite number is picked randomly each time it's used in a class method
    break_after (int, 100) : number of iterations before the loop breaks, note: only used in mass_message
    output (bool, False) : whether output generated by the class should be logged to the console or not

  Note:
    These limits are set to keep your userbot safe.
    You may override them by passing them as a keyworded-argument to the constructor.
  """


  # raises a ValueError with a prefix
  @staticmethod
  def _err(arg):
    raise ValueError("dsf::errors::" + str(arg))

  # puts a print statement out with a prefix
  @staticmethod
  def _not(arg):
    print("dsf::deforders::" + str(arg))

  # pick random number from self.wait
  # another strategy used to evade API detection
  @staticmethod
  def _wait(self,wait=list(range(60,600))):
    return random.choice(wait)

  # mass msg a channel
  @staticmethod
  async def mass_message(content, **kwargs):

    target = kwargs.get("target", None)
    break_after = kwargs.get("break_after", 100000)
    output = kwargs.get("output", False)
    
    if type(target) != discord.TextChannel:
      Deforders._err("mass_message() accepts only discord.TextChannel")
      return
    
    for i in range(break_after):
      await target.send(str(content))
      if output:
        Deforders._not(f"iteration {i}")
      await asyncio.sleep(Deforders._wait())
      # loop end ensurer
      if i == break_after:
        break

  # mass dm a guild's members
  @staticmethod
  async def mass_dm(content, **kwargs):

    # target guild
    target = kwargs.get("target", None)

    if type(target) != discord.Guild:
      Deforders._err("mass_dm() accepts only discord.Guild")
      return

    # handling kwargs

    # number of members to msg (optional) (list with elements from and to), if len(list) is 0 assume all that are present in the guild
    members_limit = kwargs.get("members", [])
    # members to ignore
    ignore = kwargs.get("ignore", [])
    # network object
    network = kwargs.get("network", None)
    # whether to display stats
    output = kwargs.get("output", False)


    # figuring out what members to msg
    if len(members_limit) == 0:
      members = target.members
    else:
      members = target.members[members_limit[0]:members_limit[1]]

    # actually doing the messaging

    count = 0
    total_members = len(members)
    network_converted = []
    if network != None:
      for m in network.workers:
        network_converted.append(m.bot.user.id)
    for member in members:
      count += 1
      wait = Deforders._wait()
      if member.bot:
        Deforders._not(f"skipped {member.name}#{member.discriminator} because of BotUser || member {count} of {total_members}")
        continue
      if isinstance(member,discord.ClientUser):
        Deforders._not(f"skipped {member.name}#{member.discriminator} because of ClientUser || member {count} of {total_members}")
        continue
      if member.id in network_converted:
        Deforders._not(f"skipped {member.name}#{member.discriminator} because of NetworkUser || member {count} of {total_members}")
        continue
      if not member.id in ignore:
        try:
          await member.send(str(content))
        except Exception as e:
          Deforders._not(f"skipped {member.name}#{member.discriminator} because of Exception: {e} || member {count} of {total_members}")
          continue
        if output:
          Deforders._not(f"messaged {member.name}#{member.discriminator} || member {count} of {total_members} || next in {wait}s")
        await asyncio.sleep(wait)
      else:
        if output:
          Deforders._not(f"ignored {member.name}#{member.discriminator} || member {count} of {total_members}")
        continue

  # scrape invites from scope
  @staticmethod
  async def scrape_invites(scope='all', **kwargs):
    timeout = kwargs.get("timeout", None)
    worker = kwargs.get("worker", None)
    ignore = kwargs.get("ignore", [])
    output = kwargs.get("output", False)
    while True:
      waiting = await worker.bot.wait_for("message", check=lambda m: "https://discord.gg/" in m.content and not m.author.id in ignore and not m.channel.id in ignore, timeout=timeout)
      try:
        await worker.bot.join_guild(str(waiting.content))
        if output:
          print(f"dsf::deforders::joined scraped invite {waiting.content}")
      except Exception as e:
        if output:
          print(f"dsf::deforders::failed to join scraped invite {waiting.content} because of Exception: {e}")
        
