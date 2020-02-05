from django.contrib import admin

# Register your models here.
from searchengine.models import DocIndex


@admin.register(DocIndex)
class DocIndexAdmin(admin.ModelAdmin):
    pass
