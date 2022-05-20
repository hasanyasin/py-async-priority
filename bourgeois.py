import random


class Member():
  def __init__(self, tasks, logger):
    self.total_output = len(tasks)
    self.tasks = tasks
    self.log = logger

  def queued(self):
    return len(self.tasks)

  def total(self):
    return self.total_output

  async def work(self):
    neworders = random.randrange(1, 3)
    self.log("business is thriving. Got %d new orders" % neworders)
    self.total_output += neworders
    self.tasks.append(self.total_output)
