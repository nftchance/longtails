import discord

from django.conf import settings

from discord.ext import commands, tasks

from coolcats.grab_most_recent import handle_scrape

class Cooltopia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.find(
            lambda g: g.name == settings.DISCORD_GUILD_NAME,
            self.bot.guilds
        )

        self.longtails_channel = discord.utils.get(
            self.guild.text_channels,
            name=settings.DISCORD_CHANNEL_NAME
        )

        self.sync_required_items.start()
        print('[Cooltopia] Online.')

    @tasks.loop(minutes=60 * 6)
    async def sync_required_items(self):
        print("[Cooltopia] [Sync] Clock.")

        required_items = handle_scrape()

        embed = discord.Embed(
            title=f"[Cooltopia] Required Items",
            description="This is the summary of the required items that will be used for boss battles within Cooltopia."
        )

        for i, item in enumerate(required_items):
            embed.add_field(name=f"Item #{i}", value=f"ID {item}")

        await self.longtails_channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Cooltopia(bot),
        guilds=[discord.Object(id=settings.DISCORD_GUILD_ID)]
    )

    print("[Cooltopia] Setup.")