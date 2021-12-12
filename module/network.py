""" network.py
for bundling the manager and worker components
"""

class Network:
  def __init__(self, manager: list, workers: list):
    self.manager = manager[0]
    self.workers = workers
    team = [self.manager]
    for i in self.workers: team.append(i)

  def _bots(self):
    temp = []
    for i in self.team: temp.append(i.bot)
    return temp

  def 
