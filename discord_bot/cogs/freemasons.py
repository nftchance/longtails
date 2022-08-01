import datetime
import django
import discord

from django.conf import settings

from discord import app_commands
from discord.ext import commands, tasks

from asgiref.sync import sync_to_async

from freemasons.models import SECONDS_BETWEEN_SYNC, FreeMasonMember, FreeMasonProject, TwitterUser
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
            title=f"[{title_key}] {project_obj.name}",
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
        print("[FreeMasons] [Sync] Clock.")

        projects = FreeMasonProject.objects.filter(
            watching=True,
        )

        for project_obj in projects.all():
            if not project_obj.next_sync_at or project_obj.next_sync_at < django.utils.timezone.now():
                print(
                    f'[FreeMasons] [Sync] [Project] {project_obj.contract_address}')
                embed = discord.Embed(
                    title=f"[SYNCING] {project_obj.name}"
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

                await project_obj.sync()

            for member in project_obj.members.filter(
                next_sync_at__lte=django.utils.timezone.now()
            ) | project_obj.members.filter(next_sync_at__isnull=True):
                print(
                    f'[FreeMasons] [Sync] [Member] {member.twitter.username}')
                await member.sync(self.twitter_client)

            if not project_obj.last_summarized_at or project_obj.last_summarized_at < django.utils.timezone.now() - datetime.timedelta(seconds=SECONDS_BETWEEN_SYNC):
                await self.send_summary('Followed By', project_obj, project_obj.member_following_summary[:50])
                await self.send_summary('Follower Of', project_obj, project_obj.member_follower_summary[:50])

                project_obj.last_summarized_at = django.utils.timezone.now()
                project_obj.save()

    @app_commands.command(name="watch")
    async def watch(self, interaction: discord.Interaction, contract_address: str) -> None:
        await interaction.response.send_message("Updating status.", ephemeral=True)

        project_obj, created = FreeMasonProject.objects.get_or_create(
            contract_address=contract_address
        )

        project_obj.watching = not project_obj.watching

        if project_obj.watching:
            await project_obj.sync()

        project_obj.save()

        embed = discord.Embed(
            title=f"[Watching] {project_obj.name}"
        )

        embed.add_field(name="CONTRACT", value=contract_address)
        embed.add_field(
            name="WATCHING",
            value="✅" if project_obj.watching else "❌",
            inline=False
        )

        await self.longtails_channel.send(embed=embed)

    @app_commands.command(name="watching")
    async def watching(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Logging statuses.", ephemeral=True)

        projects = FreeMasonProject.objects.filter(watching=True)

        embed = discord.Embed(
            title=f"[Watching] Summary",
            description="\n".join(
                f"[{project_obj.name}]({project_obj.twitter})" for project_obj in projects.all())
        )

        await self.longtails_channel.send(embed=embed)

    @app_commands.command(name="watched")
    async def watched(self, interaction: discord.Interaction, twitter_username: str) -> None:
        await interaction.response.send_message("Grabbing the data that we have for that username.")

        # get twitter object of username we are searching
        twitter_user_obj = TwitterUser.objects.filter(
            username=twitter_username)

        # return no data message if we don't have this user in the database
        if not twitter_user_obj.exists():
            embed = discord.Embed(
                title=f"[Watching] No Data Found For {twitter_username}",
            )

            await self.longtails_channel.send(embed=embed)

            return

        # find members that are following that user
        members = FreeMasonMember.objects.filter(
            following__in=[twitter_user_obj, ])

        description = "\n".join(
            [f"[{member_inst.username}](https://twitter.com/i/user/{member_inst.twitter_identifier})" for member_inst in members.all()])

        if members.count() > 50:
            description += f"\nAnd {members.count() - 50} others."

        # return output
        embed = discord.Embed(
            title=f"[Watching] Free Mason Members Following {twitter_username}",
            description=description
        )

        await self.longtails_channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        FreeMasons(bot),
        guilds=[discord.Object(id=settings.DISCORD_GUILD_ID)]
    )

    print("[FreeMasons] Setup.")
