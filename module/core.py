# dependencies
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from github import Github

# core data types
git_info = {
  author: "ezrael-git"
  repo: "discord.self.framework"
  path: f"{repo}/module/"
}


# core functions

# automatically get and evaluate the latest version from github
def git(file):
  g = Github()
  r = g.get_repo(git_info["path"])
  c = r.get_contents(file).decoded_content.decode()
  f = open(file, w)
  f.write(str(c))
  f.close()
  exec(open(file).read(), globals())



# worker.py
git("worker.py")

#manager.py
git("manager.py")


