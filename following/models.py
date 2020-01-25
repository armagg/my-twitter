from django.db import models
from django.db.models import CASCADE

from accounting.models import Account
from tweeting.models import Tweet


class Follow(models.Model):
    follower = models.ForeignKey(Account, on_delete=CASCADE, blank=False, related_name='following', db_index=True)
    followed = models.ForeignKey(Account, on_delete=CASCADE, blank=False, related_name='followed_person', db_index=True)

    class Meta:
        pass
