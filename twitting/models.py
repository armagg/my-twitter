from django.db import models
from django.db.models import PROTECT, CASCADE

from accounting.models import Account
# class Tweet(models.Model):
#     owner = models.ForeignKey(Account, verbose_name='نویسنده', blank=False, on_delete=PROTECT,
#                               related_name='owner')
#
#     title = models.CharField(max_length=140, verbose_name='عنوان', blank=False)
#
#     parent_tweet = models.ForeignKey("self", blank=True, on_delete=PROTECT, related_name='comment', null=True)
#     document = models.TextField(verbose_name='متن', name='document')
#
#     tweet_followers = models.ManyToManyField(Account, related_name='follower', blank=True)
#     likers = models.ManyToManyField(Account, related_name='liker', db_index=True, blank=True)
#
#     class Meta:
#         verbose_name = 'توییت!'
#
#
#     def get_comments(self):
#
#         children = Tweet.objects.get(parent_tweet=self)
#         return children
# from paging.models import Page
from paging.models import Page


class Tweet(models.Model):
    author = models.ForeignKey(Account, verbose_name='author', on_delete=PROTECT, related_name='author', default=None)
    document = models.TextField(verbose_name='متن', name='document')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, default=None)
    parent_tweet = models.ForeignKey("self", blank=True, on_delete=CASCADE, related_name='comment', null=True,
                                     default=None)
    date_published = models.DateTimeField(auto_now=True, blank=False)
    contributors = models.ManyToManyField(Account, related_name='contributors', blank=True)

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

        return 10

    def get_tweet_front(self, editable: bool):
        author = self.author
        return {
            'bookmark_state': False,
            'like_pack': {
                'like_numbers': self.get_like_number()
            },
            'editable': editable,
            'name': author.name,
            'avatar': '',
            'content': self.document,
            'time': self.date_published.isoformat(),
            'replies': [],
            'id': 'tweet' + str(self.id)
        }
