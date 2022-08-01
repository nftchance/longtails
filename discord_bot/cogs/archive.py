import discord
import json
import os

from discord.ext import commands

from django.conf import settings

intents = discord.Intents.all()
intents.members = True

class Archive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.find(
            lambda g: g.name == settings.DISCORD_GUILD_NAME,
            self.bot.guilds
        )

        self.archive_channel = discord.utils.get(
            self.guild.text_channels,
            name="🟣📔-archives"
        )

        print('[Archive] Online.')

    def formatted_message(self, message):
        return {
            "id": message.id,
            "author": message.author.name,
            "bot": message.author.bot,
            "message": message.content
        }

    @commands.command(aliases=['archive'])
    @commands.has_permissions(manage_messages=True)
    async def archive_command(self, ctx):
        await ctx.send('Archiving all channel messages into .json file.')

        messages = await ctx.channel.history(limit=99999).flatten()
        formatted_messages = [self.formatted_message(message) for message in messages]

        filename = f'{ctx.channel.name}.json'

        with open(filename, 'w') as json_file:
            json.dump(formatted_messages, json_file)

        output_file = discord.File(filename)

        await self.archive_channel.send(
            f"**Archived Transcript of:**\n{ctx.channel.name}", 
            file=output_file
        )
        await ctx.channel.delete()

        os.remove(filename)

def setup(bot):
    bot.add_cog(
        Archive(bot),
        guilds=[discord.Object(id=settings.DISCORD_GUILD_ID)]
    )

    print("[Archive] Setup.")