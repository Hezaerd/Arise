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

    @hunter.command(
        name="class",
        usage=">hunter class <class>",
    )
    async def choose_class(self, ctx, choice: str):
        embed = discord.Embed(title="Choose a class")
        embed.colour = discord.Colour.purple()
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar)
        embed.timestamp = ctx.message.created_at

        # Check if user is registered
        if not self.bot.db.hunters.find_one({"_id": ctx.author.id}):
            embed.colour = discord.Colour.red()
            embed.description = "You are not a hunter!\n" \
                                "Use `>hunter awake` to become a hunter!"
            await ctx.reply(embed=embed)
            return

        # Check if user already has a class (and if cooldown is over)
        if self.bot.db.hunters.find_one({"_id": ctx.author.id})["class"]:
            is_on_cooldown = self.bot.db.hunters.find_one({"_id": ctx.author.id})["class_change_cooldown"] > time.time()

            if is_on_cooldown:
                embed.colour = discord.Colour.red()
                embed.description = "You already have a class!\n" \
                                    "You can change your class once a week!\n" \
                                    f"Next change available <t:{int(self.bot.db.hunters.find_one({'_id': ctx.author.id})['class_change_cooldown'])}:R>"
                await ctx.reply(embed=embed)
                return

        # Check if choice is valid
        if choice not in EClasses.__members__:
            embed.colour = discord.Colour.red()
            embed.description = "Invalid class!\n" \
                                "Use `>hunter classes` to see available classes!"
            await ctx.reply(embed=embed)
            return

        # Set class
        self.bot.db.hunters.update_one({"_id": ctx.author.id}, {"$set": {"class": choice}})

        # Set class_change_cooldown (1 week)
        self.bot.db.hunters.update_one({"_id": ctx.author.id},
                                       {"$set": {"class_change_cooldown": time.time() + 604800}})

        embed.colour = discord.Colour.green()
        embed.description = f"You are now a {choice}!"
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Hunter(bot))
