# dependencies
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from github import Github
import os

# core data types
git_info = {
  "author": "ezrael-git",
  "repo": "discord.self.framework",
  "path": "discord.self.framework/module/"
}


# core functions

# automatically get and evaluate the latest version from github
def git(file, branch="development"):
  ghub = Github()
  repo = ghub.get_repo(git_info["author"] + "/" + git_info["repo"])
  branch = repo.get_branch(branch=branch)
  f_loaded = None
  for asd in branch.files:
    if asd.name == file:
      f_loaded = asd
  contents = repo.get_contents("/module/" + file, ref=f_loaded.sha).decoded_content.decode()
  f = open(file, "w")
  f.write(c)
  f.close()
  exec(open(file).read(), globals())
  print(c)



class dsf:
  @classmethod
  def filetype(self, name):
    valid = ["worker", "manager", "dual", "__ignore__"]
    if name in valid:
      if name != valid[2] and name != valid[3]:
        git(name + ".py")
      else:
        if name[2]:
          git("worker.py")
          git("manager.py")
        else:
          return
    else:
      raise ValueError(f"Invalid file-type: {name}")


