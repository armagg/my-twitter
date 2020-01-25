from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    location = models.TextField(max_length=60, default='iran!', )
    bio = models.TextField(max_length=120, default='nothing until now')

    def __str__(self):
        return self.user.username
