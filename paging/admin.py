from django.contrib import admin

# Register your models here.
from paging.models import Page
from django.contrib import admin


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
