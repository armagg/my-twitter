from django.contrib import admin

from alerting.models import Alert


class AlertAdmin(admin.ModelAdmin):
    pass


admin.site.register(Alert)
