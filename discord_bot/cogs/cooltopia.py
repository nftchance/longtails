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

    @tasks.loop(minutes=60 * 12)
    async def sync_required_items(self):
        print("[Cooltopia] [Sync] Clock.")

        boss_battles = handle_scrape()

        for boss_battle in boss_battles:
            embed = discord.Embed(
                title=f"[Cooltopia] [Boss Battle] {boss_battle['bosses'][0]['name']}",
            )

            embed.add_field(name="Live", value=boss_battle['live'], inline=False)
            embed.add_field(name="Location", value=boss_battle['name'], inline=False)

            embed.add_field(name="Required Items", value="\n".join(set(f"Item #{item}" for item in boss_battle['bosses'][0]['requiredItems'])), inline=False)

            embed.set_image(url=boss_battle['image'])

            await self.longtails_channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Cooltopia(bot),
        guilds=[discord.Object(id=settings.DISCORD_GUILD_ID)]
    )

    print("[Cooltopia] Setup.")