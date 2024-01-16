import time

import discord
from discord.ext import commands

from Enums.EClasses import EClasses

from Tools.Emoji import Classes
from Tools.Emoji import Stats
from Tools.Emoji import Levels

from UI.Views.Profile import PageView


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
            "name": ctx.author.name,
            "class": None,
            "level": 1,
            "xp": 0,
        })

        self.bot.db.hunters.stats.insert_one({
            "_id": ctx.author.id,
            # Life
            "max_health": 10,
            "health": 10,
            # Mana
            "max_mana": 2,
            "mana": 2,
            # Resistances
            "defence": 0,
            "magic_resistance": 0,
            # Damage
            "strength": 1,
            "intelligence": 0,
            # Secondary stats
            "agility": 0,
            "luck": 0,
        })

        self.bot.db.hunters.inventory.insert_one({
            "_id": ctx.author.id,
            "items": [],
            "weapons": [],
            "armors": [],
            "potions": [],
            "spells": [],
        })

        embed.colour = discord.Colour.green()
        embed.description = "Welcome to the hunter society!\n" \
                            "You are now a hunter!\n" \
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


    @hunter.command(
        name="profile",
        aliases=["p"],
        usage=">hunter profile",
    )
    async def profile(self, ctx):
        user = self.bot.db.hunters.find_one({"_id": ctx.author.id})
        user_stats = self.bot.db.hunters.stats.find_one({"_id": ctx.author.id})

        if user is None:
            embed = discord.Embed(title="Error")
            embed.colour = discord.Colour.red()
            embed.description = "You are not a hunter!"
            embed.add_field(name="Search how to become a hunter?", value="`>hunter awake` to join the hunter society!")
            await ctx.reply(embed=embed)
            return

        profile = discord.Embed(title=":bust_in_silhouette: Profile")
        profile.set_thumbnail(url=ctx.author.avatar)
        profile.colour = discord.Colour.purple()
        profile.set_footer(text="Last update")
        profile.timestamp = ctx.message.created_at
        profile.add_field(name=f"Class - {Classes[user['class']]}", value=f"{user['class']}", inline=False)
        profile.add_field(name=f"Level - {Levels['LVL']}", value=f"{user['level']}", inline=True)
        profile.add_field(name=f"XP - {Levels['XP']}", value=f"{user['xp']}")

        stats = discord.Embed(title=":bar_chart: Stats")
        stats.set_thumbnail(url=ctx.author.avatar)
        stats.colour = discord.Colour.pink()
        stats.set_footer(text="Last update")
        stats.timestamp = ctx.message.created_at
        stats.add_field(name=f"{Stats['HP']} HP", value=f"{user_stats['health']} / {user_stats['max_health']}")
        stats.add_field(name=f"{Stats['MP']} MP", value=f"{user_stats['mana']} / {user_stats['max_mana']}")
        stats.add_field(name="", value="", inline=False)

        stats.add_field(name=f"{Stats['DEF']} DEF", value=f"{user_stats['defence']}")
        stats.add_field(name=f"{Stats['MR']} MR", value=f"{user_stats['magic_resistance']}")
        stats.add_field(name="", value="", inline=False)

        stats.add_field(name=f"{Stats['STR']} STR", value=f"{user_stats['strength']}")
        stats.add_field(name=f"{Stats['INT']} INT", value=f"{user_stats['intelligence']}")
        stats.add_field(name="", value="", inline=False)

        stats.add_field(name=f"{Stats['AGI']} AGI", value=f"{user_stats['agility']}")
        stats.add_field(name=f"{Stats['LUK']} LUK", value=f"{user_stats['luck']}")
        stats.add_field(name="", value="", inline=False)

        embeds = [profile, stats]

        async with ctx.typing():
            await ctx.reply(embed=profile, view=PageView(embeds, ctx, self.bot))



async def setup(bot):
    await bot.add_cog(Hunter(bot))
