from django.contrib import admin

from .models import TwitterUser, FreeMasonMember, FreeMasonProject

admin.site.register(TwitterUser)
admin.site.register(FreeMasonMember)
admin.site.register(FreeMasonProject)