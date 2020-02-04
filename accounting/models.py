import random
import string

from django.contrib.auth.models import User
from django.db import models


# from paging.models import Page


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name="account")
    portfolio_site = models.URLField(default='google.com', blank=True, null=True)
    profile_photo = models.FileField(null=True, upload_to="profiles", default='/profiles/default.png')
    name = models.CharField(max_length=20, blank=False)
    location = models.TextField(max_length=60, default='iran!', null=True)
    bio = models.TextField(max_length=120, default='nothing until now')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return 'account of user by username: ' + self.user.username



class Token(models.Model):
    username = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.username + ' : ' + self.code


def create_new_token(username):
    code = get_random_code()
    token = Token(username=username, code=code)
    return token


def get_random_code():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(20))
