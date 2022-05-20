import time, asyncio


class Member():
  def __init__(self, tasks, logger):
    self.tasks = tasks
    self.log = logger
    self.skipped_breaks = []

  def wine_break(self):
    self.log("on wine break, all the work must stop")

    # even when in an async function, when you block, you block.
    # You block the whole process/thread because there is only one flow.
    time.sleep(1)

  async def soft_break(self):
    self.log("happy worker on wine break, will let others continue working")
    await asyncio.sleep(1)

  async def cleanup(self):
    done = 0
    self.log("accummulated %d breaks." % len(self.skipped_breaks))
    towait = len(self.skipped_breaks)
    while towait > 0 and towait >= len(self.tasks) and done <= 10:
      low_priority_task = self.skipped_breaks.pop()
      towait -= 1
      done += 1
      await low_priority_task

  async def work(self, with_bonus=False):
    shift = 0
    while len(self.tasks) > 0:
      self.tasks.pop()
      self.log("finished one more product. left %d" % len(self.tasks))
      shift += 1
      if shift == 2:
        break

      if with_bonus:
        self.skipped_breaks.append(self.soft_break())
        # if we called this with await, then coffee breaks would cause an endless
        # workload that can never finish because the boss keeps adding tasks
        # while we are wasting time at breaks. By calling without await, we
        # simply move on to the next cycle while this *async stack* is put on
        # hold for its coffee break.
        # If we didn't add it somewhere to be awaited later, it would have never
        # even had a chance to start because event loop would never come back to
        # this.
      else:
        self.wine_break()
