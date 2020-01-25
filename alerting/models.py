from django.db import models
from django.db.models import PROTECT

from accounting.models import Account


class Tweet(models.Model):
    owner = models.ForeignKey(Account, verbose_name='نویسنده', blank=False, on_delete=PROTECT, related_name='owner')
    contributors = models.ManyToManyField(Account, related_name='contributors')
    title = models.CharField(max_length=140, verbose_name='عنوان', blank=False)
    date_published = models.DateTimeField(auto_now=True, blank=False)
    is_root = models.BooleanField()
    parent_tweet = models.ForeignKey("self", blank=True, on_delete=PROTECT)
    document = models.TextField(verbose_name='متن', name='document')

    tweet_followers = models.ManyToManyField(Account, related_name='follower')
    likers = models.ManyToManyField(Account, related_name='liker', db_index=True)

    def get_contributors(self):
        objects = [self.owner]
        for obj in self.contributors.all():
            objects.append(obj)
        return objects
