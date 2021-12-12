# dependencies
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from github import Github
import os
from typing import Union
import random

# core data types
git_info = {
  "author": "ezrael-git",
  "repo": "discord.self.framework",
  "path": "discord.self.framework/module/"
}


# core functions

# gets sha from tag
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



# automatically get and exec() the latest commit from github

# kwargs: author, repo, branch, path, mode

# if mode is 0 (default), execute the output, else return it

def git(**kwargs):

  # handling kwargs

  author, repo, branch, path, mode = kwargs.get("author"), kwargs.get("repo"), kwargs.get("branch"), kwargs.get("path"), kwargs.get("mode")

  if author == None:

    author = git_info["author"]

  if repo == None:

    repo = git_info["repo"]

  if branch == None:

    branch = "development"

  if path == None:

    raise ValueError("Expected path: required argument")

  if mode == None:

    mode = 0

  

  ghub = Github()

  repo = ghub.get_repo(author + "/" + repo)

  branch = repo.get_branch(branch=branch)

  sha = get_sha_for_tag(repo, branch.name)

  file_content = repo.get_contents(path, ref=sha).decoded_content.decode()

  if mode == 0:

    exec(file_content, globals())

  elif mode == 1:

    return file_content

# oneline for loop for direct orders
def olfor(stop, do):
  for i in range(int(stop)):
    exec(do)
    if i == int(stop):
      return


# oneline for loop for direct orders
def olfor(stop, do):
  for i in range(int(stop)):
    exec(do)
    if i == int(stop):
      return


# utils related to the framework
class dsf:
  @classmethod
  def filetype(self, name):
    valid = ["worker", "manager", "dual", "__ignore__"]
    if name in valid:
      if name != valid[2] and name != valid[3]:
        git(path="/module/" + name + ".py")
      else:
        if name[2]:
          git(path="/module/worker.py")
          git(path="/module/manager.py")
        else:
          return
    else:
      raise ValueError(f"Invalid file-type: {name}")

  # contains all the default orders, also called deforders
  # deforders are executed directly, there is no need to worker.hear()
  class deforders:
    
    @classmethod
    def mass_msg(self, content: list, target_channel: Union[discord.TextChannel, discord.User, discord.Guild], worker_class, **kwargs):
      # kwargs
      wait = kwargs.get("wait", [60, 120, 30, 20, 10, 12, 14, 16, 34, 37, 300])
      break_after = kwargs.get("break_after", 100000)
      ignore = kwargs.get("ignore", [])
      ignore.append(worker_class.bot.user.id)
      manager_class = kwargs.get("manager", None)
      if not manager_class == None:
        manager_sendable = worker_class.bot.get_user(manager_class)
      
      # main function
      async def temp():
        await worker_class.bot.wait_until_ready()
        if isinstance(target_channel,discord.TextChannel) or isinstance(target_channel,discord.User):
          for i in range(break_after):
            if i == break_after:
              return
            await asyncio.sleep(random.choice(wait))
            await target_channel.send(random.choice(content))
        else:
          count = 0
          for member in target_channel.members:
            await asyncio.sleep(random.choice(wait))
            count += 1
            if count == break_after:
              caou = f"dsf::deforders::break_after limit reached, discontinuing loop || {count}"
              if not manager_class == None:
                await manager_sendable.send(caou)
              else:
                print(caou)
              return
            if member.id in ignore:
              iaou = f"dsf::deforders::ignoring {member.name}#{member.discriminator} || {count}"
              if not manager_class == None:
                await manager_sendable.send(iaou)
              else:
                print(iaou)
              continue
            await member.send(random.choice(content))
            maou = f"dsf::deforders::sent message to {member.name}#{member.discriminator} || {count}"
            if manager_class == None:
              print(maou)
            else:
              asyncio.sleep(random.choice(wait))
              await manager_sendable.send(maou)
            
          
      # run main func
      worker_class.bot.loop.create_task(temp())
