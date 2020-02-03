from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_save

from following.models import Follow
from liking.models import Like
from twitting.models import Tweet


@receiver(post_save, sender=Follow)
def new_follow_alert(instance):
    pass


@receiver(post_save, sender=Like)
def new_like_alert():
    pass

@receiver(post_save, sender=Tweet)
def new_tweet_alert():
    pass