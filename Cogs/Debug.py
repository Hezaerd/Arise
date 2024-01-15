import time
from typing import Literal, Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context, Greedy


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tag = __class__.__name__
        self.startup_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"Cog.{self.tag}",
                             f"Loaded in {round(time.time() - self.startup_time, 2)}s")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None):
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        embed = discord.Embed(
            title="Synced",
            description=f"Synced {ret} commands to {len(guilds)} guilds.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Guilds",
            value="\n".join(str(guild) for guild in guilds),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="reload",
        aliases=["rl"],
        usage=">reload <cog>",
        invoke_without_command=True
    )
    @commands.is_owner()
    async def reload(self, ctx: Context, cog: str):
        cog = cog.capitalize()

        embed = discord.Embed(title="Reload")

        try:
            await ctx.bot.reload_extension(f"Cogs.{cog}")
            embed.colour = discord.Colour.green()
            embed.description = f"Reloaded {cog}"
        except commands.ExtensionNotLoaded:
            embed.colour = discord.Colour.red()
            embed.description = f"{cog} is not loaded"

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Debug(bot))
