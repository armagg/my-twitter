import json

from django.contrib.auth.models import User
from django.shortcuts import render

from following.models import Follow
from paging.models import Page
from twitting.models import Tweet


def homepage(request):
    users = User.objects.all()
    channels = Page.objects.filter(personal_page=False)
    followings_tweets = []
    if request.user and request.user.is_authenticated:
        follows = Follow.objects.filter(follower=request.user.account)
        for follow in follows:
            for tweet in Tweet.objects.filter(author=follow.followed):
                followings_tweets.append(tweet.get_tweet_front(False, False))

    return render(request, 'home.html',
                  {'users': users, 'channels': channels, 'followings_tweets': followings_tweets})


def new(request):
    print(request.POST.get('data'))
    if request.POST:
        print(request.POST)
    return render(request, 'home.html')
