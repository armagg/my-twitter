from django.db import models
from django.db.models import PROTECT, CASCADE

from accounting.models import Account
from paging.models import Page


class Tweet(models.Model):
    author = models.ForeignKey(Account, verbose_name='author', on_delete=PROTECT, related_name='author', default=None)
    document = models.TextField(verbose_name='متن', name='document')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, default=None)
    parent_tweet = models.ForeignKey("self", blank=True, on_delete=CASCADE, related_name='comment', null=True,
                                     default=None)
    date_published = models.DateTimeField(auto_now=True, blank=False)
    contributors = models.ManyToManyField(Account, related_name='contributors', blank=True)
    last_like_number = models.IntegerField(blank=True, default=0)

    class Meta:
        verbose_name = 'توییت'

    def get_contributors(self):
        objects = [self.author]
        for obj in self.contributors.all():
            objects.append(obj)
        return objects

    def get_username(self):
        return self.author.user.username

    def get_like_number(self):
        from liking.models import Like
        like_number = Like.get_number_of_likes(self.id)
        self.last_like_number = like_number
        self.save()
        return like_number

    def get_tweet_front(self, editable: bool, with_replies):
        replies = []
        if with_replies:
            for reply in Tweet.objects.filter(parent_tweet=self):
                replies.append(reply.get_tweet_front(False, False))
        return {
            'bookmark_state': False,
            'like_number': self.get_like_number(),
            'editable': editable,
            'name': self.author.name,
            'avatar': '',
            'content': self.document,
            'time': self.date_published.isoformat(),
            'replies': replies,
            'id': 'tweet' + str(self.id)
        }
