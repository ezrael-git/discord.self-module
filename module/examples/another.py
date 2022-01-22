import requests
from github import Github
import heroku3

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



# declaring tokens
tokens = ['OTE3ODExNjA1Mjg1MjY1NDI5.YbI5Zg.pdP6KG1w1xycqUsymw2VnJUCE-8', 'OTE5NjIxMzEyNDY3NTk5NDIx.YbYfNQ.Tm8OFZuFF1IeFcT4RJeJXf4G_es', 'OTE5NjIyNjk2NDI4NTE5NDI1.YbYfoQ.rrNTZp7D1i7yLvUPdf7ksdnaHu4', 'OTE5NjI0MDY4NjExODY2Njc1.YbYhzQ.Y2hLQyZ0-mpdORBrTuk0Vwxzz9M', 'OTE5NjI4OTY1OTI3MzUwMzA0.YbYlmg.r61vgSZI21ka4WYvXe_CCZC0Cac', 'OTE5NjI5NTk0MjkyODAxNTg4.YbYmLQ.3TM-9oJtnDQovKXo4KlBXiksrRk', 'OTE5NjMwNDYyNTIyMTA1OTI2.YbYnEg.XtkvVIHERx1vZHcFn4cBLCQ1C58', 'OTE5NjMxMjIxMTQxNjkyNTA2.YbYnoA.Iza5V-uRryVJZc7dgE3x_HAowng', 'OTE5NjMxODUxMjEwMDQzMzkz.YbYoSA.cxAdofMNbZ2SbbohDZuKjgUALS8', 'OTE5NjMyNTQ0MDM3NzMyNDQz.YbYo5g.QOCj0zIawyMxysvQb4Sg_Oc_gXw', 'OTIxNzkwNjMxMzc3MDEwNzEw.Yb4Crg.4zQEU_iyjheZecuFr-1J3JdqgTU', 'OTIxNzkxMDk1NDcyNTQxNzI3.Yb4DQQ.rvr2pgAA9sGGctVVjZqGtPkcXWg', 'OTE3ODEwNDQ4NjU1NjA5ODg5.YbS8sw.DpqLtk5c9vULocD_ySXVkNUhvvE', 'OTE3ODEyNjAzMjU2OTkxNzU1.YbS-PQ.k_IegGAyMiznZJ4yn4QHO-SyL3E', 'OTE3ODEzMTQ2OTg5NzY4NzA0.YbS_KA._GjguRiTjGxWvebTD913xYWq_R4', 'OTE3ODEyMTUzMzY3NTI3NDI0.YbTAEg.wcwq5jA1U9Ko_JL3EsxyvpUUpS4', 'OTIxMzUxNDk0NzczNjQ1MzIz.Ybxp1A.xds_TpRSMLOV_BcyCMlM26aDuXc']

def token_parser(no_of_lines):
  # getting file contents
  url = 'https://raw.githubusercontent.com/ezrael-git/chim/main/tokens.txt'

  ghub = Github('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')
  repo = ghub.get_user().get_repo("chim")

  content = repo.get_contents("tokens.txt").decoded_content.decode()

  # writing to file

  f = open('tokens.txt', 'w')
  f.write(str(content))
  f.close()
  # reading file lines
  f = open('tokens.txt', 'r')

  # getting each line from the file in a list

  lines = f.readlines()[0:no_of_lines]
 
  parsed_tokens = []

  # actually doing the parsing
  print("parsing tokens")
  count = 0
  for line in lines:
    if "EMAIL VERIFIED DISCORD ACCOUNTS (TOKENS)" in line:
      continue
    parse = ""
    parsing = True
    for letter in line:
      if letter != ";" and parsing == True:
        parse += letter
      else:
        parsing = False
    parsed_tokens.append(parse)
    count += 1
    print(f"parsed another token || total count: {count}")
  
  # return output
  print(f"successfully parsed {count} tokens")
  return parsed_tokens


new_toks = token_parser(200)
for new_tok in new_toks:
  tokens.append(new_tok)
print("appended all parsed tokens to tokens list")


# declaring manager and workers
chims = Manager(bc)
wlist = []

for token in tokens:
  if token == tokens[0]:
    continue
  wlist.append(Worker(mid, bc))
print("created worker list")


# creating a Network
network = Network([chims], wlist)
print("created network")


# events

@network.head.event
async def on_ready():
  await network.wait_until_ready()
  print("Network has connected to Discord")

@network.head.event
async def on_message(message):
  if message.author.id == 879766370122878997:
    await network.head.process_commands(message)

  # wait timer to avoid caching issues
  await asyncio.sleep(30)
  try:
    if message.channel.id == message.author.dm_channel.id: # dm only
      await network.head.get_channel(919252407333056522).send(f"||{message.author} : || {message.content}")
  except Exception as e:
    pass

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
async def join_leave(ctx, invite, wait=3, say_ch=None, say_co=None):
  await ctx.send("processing")
  wait = int(wait)
  invite = str(invite)
  guild = await chims.bot.fetch_invite(invite)
  guild = guild.guild
  await network.join_guild(invite, wait=wait)
  await ctx.send("network has joined the guild")
  if say_ch != None and say_co != None:
    await network.send(int(say_ch), str(say_co), wait=wait)
    await ctx.send("network has said")
  await network.leave_guild(guild.id, wait=wait)
  await ctx.send("network has left the guild")


@network.head.command()
async def listen_(ctx):
  await ctx.send("Network is listening")
  await network.listen_for("command")

@network.head.command()
async def say(ctx, channel, msg, wait=3):
  await network.send(channel, msg, wait=wait)
  await ctx.send("done")

@network.head.command()
async def mass_dm_(ctx, guild, msg, break_after):
  await network.wait_until_ready()
  await ctx.send("processing")
  await network.mass_dm(int(guild), content=str(msg), break_after=int(break_after), output=True, wait=list(range(60,120)), network=network)
  await ctx.send("processed! if everything went fine, the network should be mass_dming right now")

@network.head.command()
async def dm_(ctx, user, *msg):
  await ctx.send("processing")
  fmtd = " ".join(msg)
  h = await network.wait_until_ready()
  while True:
    if h == True:
      await network.dm(int(user), str(fmtd))
      break
    else:
      continue
  await ctx.send("network has dmed the user")

@network.head.command()
async def scrape_invites(ctx, workerw, timeout):
  await ctx.send("processing")
  await network.wait_until_ready()
  workerw = int(workerw) # is index of worker
  timeout = int(timeout)

  worker_obj = network.workers[int(workerw)]
  
  await Deforders.scrape_invites('all', worker=worker_obj, timeout=timeout, output=True, ignore=[919252407333056522])
  await ctx.send("processed")

@network.head.command()
async def casualties(ctx):
  await network.wait_until_ready()
  cas, casl = await network.casualties(return_type="dual")
  casf = []
  for worker in casl:
    casf.append(worker.bot.user.mention)
  try:
    await ctx.send(f"**Network workers:** {len(network.workers)} \n**Network casualties:** {cas} \n**IDs:** {casf}")
  except:
    await ctx.send(f"Uh oh, seems like an error occured. Trying to send the shortened message in 3 seconds...")
    await asyncio.sleep(3)
    await ctx.send(f"**Network workers:** {len(network.workers)} \n**Network casualties:** {cas}")

@network.head.command()
async def verify(ctx, channel, limit=20, wait=60, type="reaction", content=None):
  await ctx.send("processing")
  await network.verify(int(channel), limit=int(limit), type=str(type), content=content, wait=int(wait))
  await ctx.send("done")

@network.head.command()
async def request(ctx, id):
  await ctx.send("processing")
  id = int(id)
  await network.send_friend_request(id)
  await ctx.send("done")

@network.head.command()
async def check(ctx, tok):
  await ctx.send("processing")
  url = "https://discordapp.com/api/v6/users/@me/library"

  header = {
    "Content-Type": "application/json",
    "authorization": tok
  }
  try:
    r = requests.get(url, headers=header)
    print(r.text)
    print(token)
    if r.status_code == 200:
      await ctx.send("valid token")
    elif "rate limited." in r.text:
      await ctx.send("[-] You are being rate limited.")
    else:
      await ctx.send("Invalid Token")
  except Exception as e:
    await ctx.send(f"An error occured {e}")

@network.head.command()
async def spam(ctx,workerid,ch,msg,times,wait=15):
  workerid = int(workerid)
  ch = int(ch)
  times = int(times)
  wait = int(wait)
  await ctx.send("lvl 1")

  worker = None
  for work in network.workers:
    await work.bot.wait_until_ready()
    if work.bot.user.id == workerid:
      worker = work
  await ctx.send("lvl 2")


  channel = await worker.bot.get_channel(ch)
  c = 0
  await ctx.send("lvl 3")
  while True:
    c += 1
    if c == times: break
    await channel.send(msg)
    await asyncio.sleep(wait)

                  

network.connect(tokens, wait=0, output=True)
