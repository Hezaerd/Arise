import time

import discord
from discord.ext import commands

from Core.Logger import Logger


class Hunter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tag = __class__.__name__
        self.startup_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"Cog.{self.tag}",
                             f"Loaded in {round(time.time() - self.startup_time, 2)}s")

    @commands.hybrid_group(
        name="hunter",
        aliases=["p"],
        usage=">hunter <subcommand>",
        invoke_without_command=False
    )
    async def hunter(self, ctx):
        pass

    @hunter.command(
        name="register",
        aliases=["reg", "r"],
    )
    async def register(self, ctx):

        embed = discord.Embed(title="Register")

        if self.bot.db.players.find_one({"_id": ctx.author.id}):
            embed.colour = discord.Colour.red()
            embed.description = "You are already registered"
            return await ctx.reply(embed=embed)

        self.bot.db.players.insert_one({
            "_id": ctx.author.id,
            "name": ctx.author.name,
        })

        embed.colour = discord.Colour.green()
        embed.description = f"Successfully registered! :white_check_mark:"
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Hunter(bot))