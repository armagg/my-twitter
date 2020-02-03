from django.db import models
from django.db.models import CASCADE, Q

from accounting.models import Account
from twitting.models import Tweet


class Like(models.Model):
    liker = models.ForeignKey(Account, related_name='liked', blank=False, on_delete=CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='liker', db_index=True, on_delete=CASCADE)

    @staticmethod
    def get_number_of_likes(tweet_id):
        likes = Like.objects.filter(tweet__id=tweet_id)
        return likes.count()

    @staticmethod
    def has_liked(user_id, tweet_id):
        like = Like.objects.filter(Q(user_id=user_id) & Q(tweet_id=tweet_id))
        return like


class Dislike(models.Model):
    disliker = models.ForeignKey(Account, related_name='disliked', blank=False, on_delete=CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='disliker', db_index=True, on_delete=CASCADE)

    @staticmethod
    def get_number_of_dislikes(tweet_id):
        likes = Like.objects.filter(tweet__id=tweet_id)
        return likes.count()

    @staticmethod
    def has_disliked(user_id, tweet_id):
        like = Like.objects.filter(Q(user_id=user_id) & Q(tweet_id=tweet_id))
        return like.count() == 1
