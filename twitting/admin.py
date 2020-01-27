from django.contrib import admin

from twitting.models import Tweet


class TweetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tweet)
