import time

from discord.ext import commands


class Test(commands.Cog):
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
    async def test(self, ctx):
        async with ctx.typing():
            ctx.reply("nothing being tested rn")


async def setup(bot):
    await bot.add_cog(Test(bot))
