from django.contrib import admin

from liking.models import Like


class AdminLike(admin.ModelAdmin):
    pass


admin.site.register(Like)
