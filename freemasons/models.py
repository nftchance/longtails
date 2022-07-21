import django
import requests
import time

from django.conf import settings
from django.contrib.postgres.aggregates import JSONBAgg
from django.db import models
from django.db.models import Q
from django.db.models import Count, OuterRef, Subquery

from .utils import needs_sync

from twitter.client import TwitterClient

"""
Designed to support docs/social/freemason-frontrunning.md

- Create FreeMasonProject
      - From that time on Longtails will watch the follower records of
        holders of that project
- Every 12 hours a clock runs to refresh the primary brand
      members and their followers and followings (alpha generators)
- We are dumping the historical records of their social network previous to
      this period which means we are only considering the most recent
      follows of the audience at all times.
- The syncing of neither the project nor the members of a project are synced
      upon save which means the clock is doing nothing more than calling
      sync() on the project and each member.
"""

URLS = {
    "TOKEN_OWNER": "https://deep-index.moralis.io/api/v2/nft/{0}/{1}/owners?chain=eth&format=decimal",
    "MEMBERS": "http://www.nftinspect.xyz/api/collections/members/{0}?limit=2000&onlyNewMembers=false"
}


class TwitterUser(models.Model):
    twitter_identifier = models.CharField(max_length=256, null=True)
    inspect_identifier = models.CharField(max_length=256, null=True)

    name = models.CharField(max_length=256, null=True)
    username = models.CharField(max_length=256)

    pfp_url = models.TextField(null=True)
    token = models.CharField(max_length=256, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FreeMasonMember(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # if needs_sync(self.last_sync_at):
        #     self.sync()

    twitter = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=256)

    followers = models.ManyToManyField(TwitterUser, related_name="followers")
    following = models.ManyToManyField(TwitterUser, related_name="following")

    last_sync_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_wallet(self):
        headers = {
            'accept': 'application/json',
            'X-API-KEY': settings.MORALIS_API_KEY
        }

        token_split = self.twitter.token.split(':')
        contract_address = token_split[1]
        token_id = token_split[2]

        response = requests.get(URLS["TOKEN_OWNER"].format(
            contract_address, token_id
        ), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['result'][0]['owner_of']

        return ""

    def get_followers(self, twitter_client):
        return twitter_client.get_followers(self.twitter.twitter_identifier)

    def get_following(self, twitter_client):
        return twitter_client.get_following(self.twitter.twitter_identifier)

    def handle_twitter_user(self, is_follower, twitter_user):
        twitter_user_obj, created = TwitterUser.objects.get_or_create(
            twitter_identifier=twitter_user['id'])

        if twitter_user_obj.name != twitter_user['name'] or twitter_user_obj.username != twitter_user['username']:
            twitter_user_obj.name = twitter_user['name']
            twitter_user_obj.username = twitter_user['username']
            twitter_user_obj.save()

        if is_follower:
            self.followers.add(twitter_user_obj)
        else:
            self.following.add(twitter_user_obj)

    def sync(self, twitter_client):
        self.wallet_address = self.get_wallet()

        self.followers.clear()
        self.following.clear()

        followers = twitter_client.get_followers(
            self.twitter.twitter_identifier)
        following = twitter_client.get_following(
            self.twitter.twitter_identifier)
        
        # catch rate limit failures and recall this function after a timeout
        if isinstance(followers, dict) or isinstance(following, dict):
            time.sleep(4)
            self.sync(twitter_client)

        for i, twitter_user in enumerate(followers + following):
            self.handle_twitter_user(i < len(followers), twitter_user)

        self.last_sync_at = django.utils.timezone.now()
        self.save()

        return {"status": 200}

    ordering = ['created_at']


class FreeMasonProject(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # if needs_sync(self.last_sync_at):
        #     self.sync()

    contract_address = models.CharField(max_length=256)
    members = models.ManyToManyField(FreeMasonMember)

    members_spotlight_count = models.PositiveIntegerField(default=150)

    last_sync_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _member_summary(self, search_field):
        twitter_user_filter = Q(**{f"{search_field}__isnull": False})
        count_field = 'count'

        twitter_users = [
            {
                "twitter_identifier": member[0],
                "count": member[1]
            } for member in self.members
                .filter(twitter_user_filter)
                .values(search_field)
                .order_by()
                .annotate(count=Count(search_field))
                .order_by(f'-{count_field}')
                .values_list(search_field, count_field)
        ]

        return twitter_users

    @property
    def member_follower_summary(self):
        return self._member_summary('followers__twitter_identifier')

    @property
    def member_following_summary(self):
        return self._member_summary('following__twitter_identifier')

    def sync(self):
        response = requests.get(URLS["MEMBERS"].format(self.contract_address))

        if response.status_code == 200:
            response_data = response.json()

            twitter_client = TwitterClient()

            members = response_data['members'][:self.members_spotlight_count]

            member_usernames = [member['username'] for member in members]
            member_twitter_ids = twitter_client.get_username_ids(
                member_usernames)

            self.members.clear()
            for i, member in enumerate(members):
                member_twitter_obj, created = TwitterUser.objects.get_or_create(
                    twitter_identifier=member_twitter_ids[i]['id'],
                    inspect_identifier=member['id']
                )

                member_twitter_obj.name = member['name']
                member_twitter_obj.username = member['username']
                member_twitter_obj.pfp_url = member['pfpUrl']
                member_twitter_obj.token = member['token']
                member_twitter_obj.save()

                member_obj, created = FreeMasonMember.objects.get_or_create(
                    twitter=member_twitter_obj,
                )

                self.members.add(member_obj)

            self.last_sync_at = django.utils.timezone.now()
            self.save()

            return {"status": 200}
        return {"status": 500}
