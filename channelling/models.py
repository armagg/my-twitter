from django.db import models
from django.db.models import CASCADE

from accounting.models import Account
from twitting.models import Tweet


class Channel(models.Model):
    name = models.CharField(max_length=128, blank=False)
    owner = models.ForeignKey(Account, on_delete=CASCADE)
    description = models.TextField(verbose_name='توضیحات')
    admins = models.ManyToManyField(Account, related_name='authors')
    tweets = models.ManyToManyField(Tweet, related_name='posts')

