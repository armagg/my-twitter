from django.contrib import admin

from channelling.models import Channel


class ChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Channel)
