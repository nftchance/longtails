import datetime
import django
import discord

from django.conf import settings

from discord import app_commands
from discord.ext import commands, tasks

from asgiref.sync import sync_to_async

from freemasons.models import SECONDS_BETWEEN_SYNC, FreeMasonProject
from twitter.client import TwitterClient


class FreeMasons(commands.Cog):
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

        self.twitter_client = TwitterClient()

        self.sync_projects.start()
        print('[FreeMasons] Online.')

    async def send_summary(self, title_key, project_obj, summary):
        embed = discord.Embed(
            title=f"FREEMASONS {title_key} SUMMARY",
            description="\n".join(
                [f"[{member_inst['username']}](https://twitter.com/i/user/{member_inst['twitter_identifier']}): {member_inst['count']}" for member_inst in summary])
        )

        embed.add_field(
            name="CONTRACT",
            value=project_obj.contract_address
        )

        await self.longtails_channel.send(embed=embed)

    @tasks.loop(seconds=60)
    async def sync_projects(self):
        print("[FreeMasons] Syncing projects.")

        projects = FreeMasonProject.objects.filter(
            watching=True,
        )

        for project_obj in projects.all():
            if not project_obj.next_sync_at or project_obj.next_sync_at < django.utils.timezone.now():
                embed = discord.Embed(
                    title=f"FREEMASONS SYNC"
                )

                embed.add_field(
                    name="CONTRACT",
                    value=project_obj.contract_address
                )

                embed.add_field(
                    name="STATUS",
                    value="STARTING",
                    inline=False
                )

                await self.longtails_channel.send(embed=embed)

                project_obj.sync()

            for member in project_obj.members.filter(
                next_sync_at__lte=django.utils.timezone.now()
            ) | project_obj.members.filter(next_sync_at__isnull=True):
                print(f'[FreeMasons] {member.twitter.username}')
                member.sync(self.twitter_client)

            if not project_obj.last_summarized_at or project_obj.last_summarized_at < django.utils.timezone.now() - datetime.timedelta(seconds=SECONDS_BETWEEN_SYNC):
                await self.send_summary('FOLLOWING', project_obj, project_obj.member_following_summary[:25])
                await self.send_summary('FOLLOWER', project_obj, project_obj.member_follower_summary[:25])

                project_obj.last_summarized_at = django.utils.timezone.now()
                project_obj.save()

    @app_commands.command(name="watch")
    async def watch(self, interaction: discord.Interaction, contract_address: str) -> None:
        project_obj, created = FreeMasonProject.objects.get_or_create(
            contract_address=contract_address
        )

        project_obj.watching = not project_obj.watching

        project_obj.save()

        embed = discord.Embed(
            title=f"FREEMASONS WATCH UPDATE"
        )

        embed.add_field(name="CONTRACT", value=contract_address)
        embed.add_field(
            name="WATCHING",
            value="✅" if project_obj.watching else "❌",
            inline=False
        )

        await self.longtails_channel.send(embed=embed)

        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        FreeMasons(bot),
        guilds=[discord.Object(id=settings.DISCORD_GUILD_ID)]
    )

    print("[FreeMasons] Setup.")
