from django.contrib import admin

from accounting.models import Account, Token


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass