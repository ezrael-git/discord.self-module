# dependencies
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from github import Github
import os

# core data types
git_info = {
  author: "ezrael-git"
  repo: "discord.self.framework"
  path: f"{repo}/module/"
}


# core functions

# automatically get and evaluate the latest version from github
def git(file):
  if os.path.exists("./" + file) == True:
    return
  g = Github()
  r = g.get_repo(git_info["path"])
  c = r.get_contents(file).decoded_content.decode()
  f = open(file, w)
  f.write(str(c))
  f.close()
  exec(open(file).read(), globals())



class dsf:
  @classmethod
  def filetype(self, name):
    valid = ["worker", "manager", "__ignore__"]
    if name in valid:
      git(name)
    else:
      raise ValueError(f"Invalid file-type: {name}")


