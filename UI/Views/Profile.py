import discord
from discord.ext import commands


class PageSelect(discord.ui.Select):
    def __init__(self, embeds: list, ctx: commands.Context, bot: commands.Bot):
        self.bot = bot
        self.invoke_ctx = ctx
        self.profile = embeds[0]
        self.stats = embeds[1]

        options = [
            discord.SelectOption(label="Profile", description="Display hunter information", emoji="👤"),
            discord.SelectOption(label="Stats", description="Display hunter stats", emoji="📊"),
        ]

        super().__init__(placeholder="Select a page...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):

        if interaction.user != self.invoke_ctx.author:
            await interaction.response.send_message("This is not your profile!", ephemeral=True)
            return

        if self.values[0] == "Profile":
            await interaction.response.edit_message(embed=self.profile)
        elif self.values[0] == "Stats":
            await interaction.response.edit_message(embed=self.stats)


class PageView(discord.ui.View):
    def __init__(self, embeds: list, ctx: commands.Context, bot: commands.Bot):
        super().__init__()

        self.add_item(PageSelect(embeds, ctx, bot))
