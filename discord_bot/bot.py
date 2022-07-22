import discord
import django
import os

from discord.ext import commands

os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', "true")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "longtails.settings")
django.setup()

# exec(open('discord_bot/bot.py').read())

from django.conf import settings

intents = discord.Intents.all()
intents.members = True

class DiscordClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=settings.DISCORD_APPLICATION_ID
        )

    async def setup_hook(self):
        await self.load_extension(f'discord_bot.cogs.freemasons')
        await discord_client.tree.sync(guild=discord.Object(id=settings.DISCORD_GUILD_ID))

    async def on_ready(self):
        print("[Discord Client] Online.")

discord_client = DiscordClient()
discord_client.run(settings.DISCORD_TOKEN)