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
def get_sha_for_tag(repository, tag):      
    branches = repository.get_branches()                             
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:                     
        return matched_branches[0].commit.sha
                                                       
    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:                                 
        raise ValueError("No Tag or Branch exists with that name")
    return matched_tags[0].commit.sha


# built-in dependency installer
def git(file, branch="development"):
  ghub = Github()
  repo = ghub.get_repo(git_info["author"] + "/" + git_info["repo"])
  branch = repo.get_branch(branch=branch)

  target = "/module/" + file
  sha = get_sha_for_tag(repo, branch.name)

  file_content = repo.get_contents(target, ref=sha).decoded_content.decode()

  exec(file_content, globals())
  print(file_content)

# oneline for loop for direct orders
def olfor(stop, do):
  for i in range(int(stop)):
    exec(do)
    if i == int(stop):
      return


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


