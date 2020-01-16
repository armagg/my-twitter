# dappx/admin.py
from django.contrib import admin
from account.models import UserProfileInfo, User

# Register your models here.
admin.site.signup(UserProfileInfo)
