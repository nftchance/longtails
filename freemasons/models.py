import datetime
import django

from django.db import models

from requests import request

# Designed to support docs/social/freemason-frontrunning.md
# Create FreeMasonProject
#       - From that time on Longtails will watch the follower records of 
#         holders of that project
# Every 12 hours a clock runs to refresh the primary brand 
#       members (alpha generators)

# 12 hours
SECONDS_BETWEEN_SYNC = 60 * 60 * 12

class TwitterUser(models.Model):
    username = models.CharField(max_length=256)
    global_followings = models.PositiveIntegerField(default=0)
    global_followers = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FreeMasonMember(models.Model):
    twitter = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=256)

    followers = models.ManyToManyField(TwitterUser, related_name="followers")
    following = models.ManyToManyField(TwitterUser, related_name="following")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FreeMasonProject(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.needs_sync:
            self.sync()

    contract_address = models.CharField(max_length=256)
    members = models.ManyToManyField(FreeMasonMember)

    last_sync_at = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def needs_sync(self):
        return self.last_sync_at - datetime.timedelta(seconds=SECONDS_BETWEEN_SYNC) > django.utils.timezone.now()

    def sync(self):
        url = f"http://nftinspect.xyz/{self.contract_address}/members"
        response = request.get(url)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            self.last_sync_at = django.utils.timezone.now()
            self.save()
        else:
            pass
