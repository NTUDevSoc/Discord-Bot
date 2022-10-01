from __future__ import annotations

import platform
import sys
import traceback
from typing import Any, TYPE_CHECKING

import aiohttp
import discord
from discord.ext import commands
import asyncpg
import toml

from cogs import COGS
from logger import Logger

if TYPE_CHECKING:
    from logger import Logger
    from asyncpg import Pool


class DevBot(commands.Bot):
    logger: Logger
    session: aiohttp.ClientSession
    pool: Pool
    error_hook: discord.Webhook
    yellow = 0xE7EC11
    red = 0xFB5F5F

    def __init__(self) -> None:
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            message_content=True,
            presences=True,
            typing=True,
        )
        self.logger = Logger("DevSocBot", console=True)
        self._is_ready = False
        self.start_time = discord.utils.utcnow()
        self.config = toml.load("config.toml")

        super().__init__(
            command_prefix=".",
            intents=intents,
            description="DevBot",
            owner_ids=[83616065854115840, 957437570546012240],
        )

    async def on_ready(self) -> None:
        if self._is_ready:
            self.logger.info(
                f"Bot received reconnect event at {discord.utils.utcnow()}"
            )
            return
        self.logger.info(f"{self.user} is now Online!")

    async def setup_hook(self) -> None:
        headers = {
            "User-Agent": f"DevSoc Bot(https://devsoc.co.uk/) CPython/{platform.python_version()} aiohttp/{aiohttp.__version__}"
        }
        self.session = aiohttp.ClientSession(headers=headers)
        self.error_hook = discord.Webhook.from_url(
            self.config["logs"]["error"], session=self.session
        )

        self.pool = await asyncpg.create_pool(self.config["database"]["psql_uri"])  # type: ignore
        for cog in COGS:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Loaded {cog.removeprefix('cogs.')}")
            except Exception as e:
                self.logger.critical(
                    f"Exception {e} in loading {cog.removeprefix('cogs.')}"
                )
                continue

    async def start(self) -> None:
        self.logger.info("Starting Bot...")
        try:
            await super().start(self.config["bot"]["token"])
        finally:
            await self.session.close()
            await self.pool.close()
            self.logger.info("Shutdown Bot")

    async def on_error(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        error = sys.exc_info()[1]
        if error:
            error_type = type(error)
            trace = error.__traceback__
            error_message = "".join(
                traceback.format_exception(error_type, error, trace)
            )
            event_name = event.title().replace("_", " ")
            error_name = error_type.__name__
            self.logger.warning(
                f"ERROR IN EVENT: {event_name}. {error_name}\n{error_message}"
            )
            embed = discord.Embed(
                title="An Error Occurred",
                description=f"**__Event:__** {event_name}\n"
                f"**__Error:__** {error_name}\n```py\n{error_message}\n```",
                colour=self.red,
                timestamp=discord.utils.utcnow(),
            )
            assert self.user is not None
            await self.error_hook.send(
                embed=embed,
                avatar_url=self.user.avatar.url,  # type: ignore
                username=f"{self.user} | Error Logs",
            )
            return await super().on_error(event, *args, **kwargs)
