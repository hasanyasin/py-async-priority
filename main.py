import asyncio
import proletarian, bourgeois, logger


def logger(cls, color):
  return lambda msg: print("\033[%dm%s:\x1B[0m %s" % (color, cls, msg))


async def main(cycle):
  tasks = [a for a in range(1, 11)]

  hgh = bourgeois.Member(tasks, logger("boss", 91))
  low = proletarian.Member(tasks, logger("worker", 92))

  while len(tasks) > 0:
    await cycle(hgh, low)
    print(
      "End of a cycle. Left %d tasks. Earned lots of money with %d products." %
      (len(tasks), hgh.total()))


async def natural_cycle(hgh, low):
  await hgh.work()
  await low.work()


async def modern_cycle(hgh, low):
  if hgh.queued() < 100:  # we don't want to have too many open orders
    await hgh.work()

  await low.work(True)
  await low.cleanup()  # lower priority work!


asyncio.run(main(natural_cycle))
# asyncio.run(main(modern_cycle))
