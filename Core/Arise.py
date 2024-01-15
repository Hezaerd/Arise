import discord
from discord.ext import commands
import os

from Core.Logger import Logger
from Core.DataBase import DataBase


class Arise(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=">", intents=discord.Intents.all(), help_command=None)

        self.logger = Logger()
        self.db = DataBase().client.heza

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        """Starts the bot"""
        await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        """Closes the bot"""
        await super().close()

    async def on_ready(self) -> None:
        """Event that fires when the bot is ready"""
        self.logger.info("Core", f"Logged in as {self.user}")

    async def load_all_extensions(self) -> None:
        """Loads all extensions"""
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"Cogs.{filename[:-3]}")

        self.logger.info("Core", "Started loading all extensions")

    async def unload_all_extensions(self) -> None:
        """Unloads all extensions"""
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                await self.unload_extension(f"Cogs.{filename[:-3]}")

        self.logger.info("Core", "Started unloading all extensions")

    async def reload_all_extensions(self) -> None:
        """Reloads all extensions"""
        await self.unload_all_extensions()
        await self.load_all_extensions()
        self.logger.info("Core", "Reloaded all extensions")
