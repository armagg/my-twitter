import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from paging.models import Page
from twitting.models import Tweet


@login_required
def page(request, page_id):
    page = Page.objects.get(page_id=page_id)
    return get_page(request, page)


def get_page(request, page):
    tweets = Tweet.objects.filter(page=page, parent_tweet=None)
    user = request.user
    comments = []
    for tweet in tweets:
        editable = (user.account == tweet.author)
        comments.append(tweet.get_tweet_front(editable, True))

    can_write = user.account in page.get_all_admins()
    data = {'comments': comments, 'comments_json': json.dumps(comments), 'title': page.title,
            'can_write': can_write, 'description': page.description, 'page_id': page.page_id}
    return render(request, './twitting/commentsPage.html', data)


@login_required
def my_page(request):
    page = Page.objects.get(page_id=request.user.username)
    return get_page(request, page)


def get_tweet_page(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    user = request.user
    comments = [tweet.get_tweet_front(user.account == tweet.author, True)]
    data = {'comments': comments, 'comments_json': json.dumps(comments),
            'title': 'replies of ' + tweet.author.name + 'posts',
            'can_write': False}  # todo: check this shit!!!!
    return render(request, './twitting/commentsPage.html', data)
