from django.db import models

# Designed to support docs/social/freemason-frontrunning.md
# Create FreeMasonProject
#       - From that time on Longtails will watch the follower records of 
#         holders of that project
# Every 12 hours a clock runs to refresh the primary brand 
#       members (alpha generators)

class TwitterUser(models.Model):
    username = models.CharField(max_length=256)
    global_followings = models.PositiveIntegerField(default=0)
    global_followers = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FreeMasonMember(models.Model):
    twitter = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=256)

    followers = models.ManyToManyField(TwitterUser)
    following = models.ManyToManyField(TwitterUser)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FreeMasonProject(models.Model):
    contract_address = models.CharField(max_length=256)
    members = models.ManyToManyField(FreeMasonMember)

    last_sync_at = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sync(self):
