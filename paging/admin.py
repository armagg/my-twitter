from paging.models import Page
from django.contrib import admin


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
