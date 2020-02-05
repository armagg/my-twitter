from django.contrib import admin

from liking.models import Like, Dislike


class AdminLike(admin.ModelAdmin):
    pass


class AdminDislike(admin.ModelAdmin):
    pass


admin.site.register(Like)
admin.site.register(Dislike)
