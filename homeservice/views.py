import json

from django.contrib.auth.models import User
from django.shortcuts import render

from following.models import Follow, FollowPage
from paging.models import Page
from twitting.models import Tweet


def homepage(request):
    users = User.objects.all()
    channels = Page.objects.filter(personal_page=False).all()

    followings_users_tweets = []
    if request.user and request.user.is_authenticated:
        followeds = Follow.objects.filter(follower=request.user.account).values_list('followed', flat=True)
        for followed in followeds:
            for tweet in Tweet.objects.filter(author=followed):
                followings_users_tweets.append(tweet.get_tweet_front(False, False))
    most_liked_tweets = []
    for tweet in Tweet.get_most_liked_tweets():
        most_liked_tweets.append(tweet.get_tweet_front(False, False))

    following_pages_tweets = []
    if request.user and request.user.is_authenticated:
        followedPages = FollowPage.objects.filter(follower=request.user.account).values_list('followed', flat=True)
        for followedPage in followedPages:
            for tweet in Tweet.objects.filter(page=followedPage):
                following_pages_tweets.append(tweet.get_tweet_front(False, False))

    return render(request, 'home.html',
                  {'users': users, 'channels': channels, 'followings_users_tweets': followings_users_tweets,
                   'most_liked_tweets': most_liked_tweets, 'following_pages_tweets': following_pages_tweets})

