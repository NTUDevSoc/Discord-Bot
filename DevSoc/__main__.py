import asyncio
import os

from . import DevBot

os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"
os.environ["JISHAKU_HIDE"] = "true"
# Jishaku is a debugging tool for discord.py
# Adds a .jsk command group that only bot owners can use.


async def main():
    bot = DevBot()
    await bot.start()


asyncio.run(main())
