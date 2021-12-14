# deforder.py

# contains all the default orders, also called deforders
# deforders are executed directly, there is no need to worker.hear()



class Deforders:
  def __init__(self, target, **kwargs):
    # kwarg handling
    """
    These limits are set to keep your userbot safe.
    You may override them by passing them as a keyworded-argument to the method.
    """

    wait = kwargs.get("wait", 10)
    break_after = kwargs.get("break_after", 100)
    output = kwargs.get("output", False)

    # self declarations
    self.target = target
    self.wait = int(wait)
    self.break_after = int(break_after)
    self.type = type(target)
    self.output = output

  # raises a ValueError with a prefix
  def _err(self, arg):
    raise ValueError("dsf::errors::" + str(arg))

  # puts a print statement out with a prefix
  def _not(self, arg):
    print("dsf::deforders::" + str(arg))

  # mass msg a channel
  async def mass_message(self, content):
    if self.type != discord.TextChannel:
      self._err("mass_message() accepts only discord.TextChannel")
      return
    
    for i in range(self.break_after):
      await self.target.send(str(content))
      if self.output:
        self._not(f"iteration {i}")
      await asyncio.sleep(self.wait)
      # loop end ensurer
      if i == self.break_after:
        break

  # mass dm a guild's members
  async def mass_dm(self, content, **kwargs):
    if self.type != discord.Guild:
      self._err("mass_dm() accepts only discord.Guild")
      return

    # handling kwargs

    # number of members to msg (optional) (list with elements from and to), if 0 assume all that are present in the guild
    members_limit = kwargs.get("members", 0)
    # members to ignore
    ignore = kwargs.get("ignore", [])

    # figuring out what members to msg
    if members_limit == 0:
      members = self.target.members
    else:
      members = self.target.members[members_limit[0]:members_limit[1])

    # actually doing the messaging

    count = 0
    total_members = len(members)
    for member in members:
      count += 1
      if not member.id in ignore:
        await member.send(str(content))
        if self.output:
          self._not(f"messaged {member.name}#{member.discriminator} || member {count} of {total_members}")
        await asyncio.sleep(self.wait)
      else:
        if self.output:
          self._not(f"ignored {member.name}#{member.discriminator} || member {count} of {total_members}")
        continue
