"""
Building a simple network that has basic functionality.
This script merges the two components - manager and workers - into one script.
This is the recommended way to operate your Network.
"""



import requests
from github import Github

# get sha from tag
def get_sha_for_tag_core(repository, tag):      
    branches = repository.get_branches()                             
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:                     
        return matched_branches[0].commit.sha
                                                       
    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:                                 
        raise ValueError("No Tag or Branch exists with that name")
    return matched_tags[0].commit.sha


# automatically get and install core.py from development branch
def download_core_py(**kwargs):
  ghub = Github()
  repo = ghub.get_repo("ezrael-git/discord.self.framework")
  branch = repo.get_branch(branch="development")

  sha = get_sha_for_tag_core(repo, branch.name)

  c = repo.get_contents("/module/core.py", ref=sha).decoded_content.decode()

  return c

c = download_core_py()
exec(c, globals())



# declaring filetype
dsf.filetype("dual")
bc = 917800718969221200 # base channel
mid = 917811605285265429 # manager id

# declaring manager and workers
chims = Manager(bc)
atob = Worker(mid, bc)
bfare = Worker(mid, bc)
sofargone = Worker(mid, bc)
fannyfred = Worker(mid, bc)
wlist = [chims, atob, bfare, sofargone, fannyfred]

# creating a Network
network = Network([chims], wlist)

# declaring tokens
tokens = ["abcd", "efg", "hijk", "lmnop", "qrst"]

# events

@network.head.event
async def on_ready():
  await network.wait_until_ready()
  print("Network has connected to Discord")

@network.head.event
async def on_message(message):
  await network.head.process_commands(message)

  # wait timer to avoid caching issues
  await asyncio.sleep(30)
  try:
    if message.channel.id == message.author.dm_channel.id: # dm only
      await network.head.get_channel(919252407333056522).send(f"||{message.author} : || {message.content}")
  except Exception as e:
    e = str(e)
    if "no attribute" in e:
      if "dsf::deforders::" in message.content and message.author.id != network.head.user.id:
        await network.head.get_channel(919252407333056522).send(f"||{message.author} : || {message.content}")
    else:
      print(f"error in on_message body: {e}")



# preparing the team

async def master():
  for member in network.team:
    await member.bot.wait_until_ready()
    await member.prep()

network.head.loop.create_task(master())

# commands

@network.head.command()
async def command(ctx, com):
  await chims.base.send(com)
  await ctx.send("done")

@network.head.command()
async def do_yourself(ctx, com):
  exec(com)
  await ctx.send("done")

@network.head.command()
async def mass_msg(ctx, use, content, target, wait=60, break_after=100000):
  await ctx.send("received")
  await network.head.wait_until_ready()
  content = content.split(':')
  ignore = []
  for member in network.team:
    ignore.append(member.bot.user.id)

  for member in network.team:
    if member.bot.user.id == int(use):
      user = member
  try:
    dsf.deforders.mass_msg(content, user.bot.get_guild(int(target)), member, wait=wait, break_after=break_after, ignore=ignore, manager=network.head.user.id)
  except UnboundLocalError:
    await ctx.send("Couldn't find that network.team member")
  await ctx.send("done")

@network.head.command()
async def join_guild(ctx, invite, wait=60):
  await network.join_guild(invite, wait=wait)
  await ctx.send("Network has joined the guild")

@network.head.command()
async def leave_guild(ctx, id, wait=60):
  await network.leave_guild(id, wait=wait)
  await ctx.send("Network has left the guild")

@network.head.command()
async def listen_(ctx):
  await ctx.send("Network is listening")
  await network.listen_for("command")

# run the team
network.connect()
