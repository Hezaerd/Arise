import time

import discord
from discord.ext import commands

from Core.Logger import Logger
from Tools.Emoji import Classes


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
        aliases=["h"],
        usage=">hunter <subcommand>",
        invoke_without_command=False
    )
    async def hunter(self, ctx):
        pass

    @hunter.command(
        name="awake",
        aliases=["register"],
    )
    async def awake(self, ctx):

        embed = discord.Embed(title="Awake")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        if self.bot.db.players.find_one({"_id": ctx.author.id}):
            embed.colour = discord.Colour.red()
            embed.description = "You are already a hunter! :x:"
            return await ctx.reply(embed=embed)

        self.bot.db.players.insert_one({
            "_id": ctx.author.id,
            "name": ctx.author.name,
        })

        embed.colour = discord.Colour.purple()
        embed.description = f"Welcome to the beautiful world of hunters :white_check_mark:"
        await ctx.reply(embed=embed)

    @hunter.command(
        name="classes",
        usage=">hunter classes",
    )
    async def classes(self, ctx):
        embed = discord.Embed(title="Available classes")
        embed.colour = discord.Colour.purple()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.timestamp = ctx.message.created_at

        embed.add_field(name=f"{Classes['Assassin']} Assassin", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Fighter']} Fighter", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Healer']} Healer", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Mage']} Mage", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Ranger']} Ranger", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Tank']} Tank", value="todo", inline=False)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Hunter(bot))