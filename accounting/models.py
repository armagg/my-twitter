
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name="account")
    portfolio_site = models.URLField(default='google.com', blank=True, null=True)
    profile_photo = models.FileField(null=True, upload_to="profiles", default='/profiles/default.png')
    name = models.CharField(max_length=20, blank=False)
    location = models.TextField(max_length=60, default='iran!', null=True)
    bio = models.TextField(max_length=120, default='nothing until now')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


