from django.db.models.signals import post_save
from django.dispatch import receiver

from alerting.models import Alert
from following.models import Follow
from liking.models import Like
from twitting.models import Tweet


@receiver(post_save, sender=Follow, weak=False, dispatch_uid='alerting.new_follow_alert')
def new_follow_alert(sender, instance: Follow, created: bool, **kwargs):
    if not created:
        return None
    alert = Alert(type=Alert.Type.NEW_FOLLOWER,
                  who=instance.follower,
                  account=instance.followed
                  )
    alert.save()


@receiver(post_save, sender=Like, weak=False)
def new_like_alert(sender, instance: Like, created: bool, **kwargs):
    if not created:
        return None
    alert = Alert(type=Alert.Type.NEW_LIKE,
                  who=instance.liker,
                  account=instance.tweet.author,
                  tweet=instance.tweet
                  )
    alert.save()


@receiver(post_save, sender=Tweet, weak=False)
def new_tweet_alert(sender, instance: Tweet, created: bool, **kwargs):
    if not created:
        return None
