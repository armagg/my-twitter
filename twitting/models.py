from datetime import datetime, timedelta

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
    plain_text = models.TextField(blank=True, null=True, default='')
    last_like_number = models.IntegerField(default=0)

    def can_access(self, username):
        if str(self.author.user.username) == str(username):
            return True
        if self.parent_tweet:
            return False
        for admin in self.page.admins.all():
            if str(admin.user.username) == str(username):
                return True
        return False

    def __str__(self):
        return self.plain_text

    def get_like_number(self):
        from liking.models import Like, Dislike
        like_number = Like.objects.filter(tweet=self).count()
        dislike_number = Dislike.objects.filter(tweet=self).count()
        return like_number - dislike_number

    def update_like_number(self):
        self.last_like_number = self.get_like_number()
        self.save()

    def get_tweet_front(self, editable: bool, with_replies):
        replies = []
        if with_replies:
            for reply in Tweet.objects.filter(parent_tweet=self):
                replies.append(reply.get_tweet_front(False, False))
        return {
            'bookmark_state': False,
            'like_number': self.last_like_number,
            'editable': editable,
            'name': self.author.name,
            'avatar': self.author.profile_photo.url,
            'content': self.document,
            'time': self.date_published.isoformat(),
            'replies': replies,
            'id': 'tweet' + str(self.id),
            'username': self.author.user.username,
            'plain_text': self.plain_text,
            'origin_id': str(self.id),
        }

    @staticmethod
    def get_most_liked_tweets():
        tweets = Tweet.objects.filter(date_published__gt=datetime.today() - timedelta(days=30)).order_by(
            '-last_like_number')[:5]
        return tweets
