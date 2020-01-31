from django.contrib import admin

from accounting.models import Account, Token


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass

