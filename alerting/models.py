from django.db import models
from django.db.models import CASCADE, Q

from accounting.models import Account
from twitting.models import Tweet


class Alert(models.Model):
    class Type(models.TextChoices):
        NEW_FOLLOWER = 'new_follower'
        NEW_LIKE = 'new_like'
        NEW_POST = 'new_post'

    type = models.CharField(max_length=20, blank=False, choices=Type.choices)
    seen = models.BooleanField(default=False, blank=False)
    account = models.ForeignKey(Account, on_delete=CASCADE, related_name='alerts', db_index=True)
    who = models.ForeignKey(Account, on_delete=CASCADE, related_name='created_alerts')
    tweet = models.ForeignKey(Tweet, on_delete=CASCADE, related_name='tweet_alert', null=True)

    @staticmethod
    def get_alerts(user_id):
        alerts = Alert.objects.filter(Q(account__user_id=user_id) & Q(seen=False))
        # for alert in alerts:
            # alert.seen = True
            # alert.save()
        return alerts



    def __str__(self):
        temp_str = self.who.name + ' has '
        if self.type == self.Type.NEW_FOLLOWER:
            return temp_str + 'followed you'
        if self.type == self.Type.NEW_LIKE:
            return temp_str + 'liked your tweet: ' + str(self.tweet)
        return temp_str + 'twitted a new post'

    def get_link_for_alert(self):
        if self.type == self.Type.NEW_FOLLOWER:
            return '/accounting/profile/' + self.who.user.username

        return '/paging/tweet/' + str(self.tweet.id)
