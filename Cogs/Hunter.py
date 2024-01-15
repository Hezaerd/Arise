import time

import discord
from discord.ext import commands

from Enums.EClasses import EClasses

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
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar)

        # Check if user is already registered
        if self.bot.db.hunters.find_one({"_id": ctx.author.id}):
            embed.colour = discord.Colour.red()
            embed.description = "You are already a hunter!"
            await ctx.reply(embed=embed)
            return

        # Register user
        self.bot.db.hunters.insert_one({
            "_id": ctx.author.id,
            "class": None,
        })

        embed.colour = discord.Colour.green()
        embed.description = "You are now a hunter!\n" \
                            "Use `>hunter classes` to see available classes!."

        await ctx.reply(embed=embed)

    @hunter.command(
        name="classes",
        usage=">hunter classes",
    )
    async def classes(self, ctx):
        embed = discord.Embed(title="Available classes")
        embed.colour = discord.Colour.purple()
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar)
        embed.timestamp = ctx.message.created_at

        embed.add_field(name=f"{Classes['Assassin']} Assassin", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Fighter']} Fighter", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Healer']} Healer", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Mage']} Mage", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Ranger']} Ranger", value="todo", inline=False)
        embed.add_field(name=f"{Classes['Tank']} Tank", value="todo", inline=False)

        embed.add_field(name="\nHow to choose a class?", value="Use `>hunter class <class>`", inline=False)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Hunter(bot))