import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from following.models import FollowPage
from paging.models import Page
from twitting.models import Tweet


@login_required
def page(request, page_id):
    q = Page.objects.filter(page_id=page_id)
    if not q.exists():
        from django.http import HttpResponse
        return HttpResponse(status=404)
    page = q.get()
    return get_page(request, page)


def get_page(request, page):
    comments = []
    for tweet in Tweet.objects.filter(page=page, parent_tweet=None):
        editable = False
        if request.user:
            editable = tweet.can_access(request.user.username)
        comments.append(tweet.get_tweet_front(editable, True))
    can_write = False
    if request.user:
        can_write = request.user.account in page.get_all_admins()
    data = {'comments': comments, 'comments_json': json.dumps(comments), 'title': page.title,
            'can_write': can_write, 'description': page.description, 'page_id': page.page_id, 'type': 'page'}
    return render(request, './twitting/commentsPage.html', data)


@login_required
def my_page(request):
    # try:
    page = Page.objects.get(page_id=request.user.username)
    return get_page(request, page)
    # except Exception as e:
    # print(e)
    # return HttpResponse(status=404)


def get_tweet_page(request, tweet_id):
    q = Tweet.objects.filter(id=tweet_id)
    if not q.exists():
        return HttpResponse(status=404)
    tweet = Tweet.objects.get(id=tweet_id)
    editable = False
    if request.user:
        if request.user.account == tweet.author:
            editable = True
    comments = [tweet.get_tweet_front(editable, True)]
    data = {'comments': comments, 'comments_json': json.dumps(comments),
            'title': 'replies of ' + tweet.author.name + ' posts',
            'can_write': False, 'type': 'tweet'}
    return render(request, './twitting/commentsPage.html', data)
