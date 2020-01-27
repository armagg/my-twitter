from django.contrib import admin

from following.models import Follow


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Follow)
