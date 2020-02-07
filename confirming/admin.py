from confirming.models import ConfirmRequest
from django.contrib import admin


@admin.register(ConfirmRequest)
class AdminConfirmation(admin.ModelAdmin):
    pass