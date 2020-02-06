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
    if not q.exist():
        from django.http import HttpResponse
        return HttpResponse(status=404)
    page = q.get()
    return get_page(request, page)


def get_page(request, page):
    tweets = Tweet.objects.filter(page=page, parent_tweet=None)
    comments = []
    for tweet in tweets:
        editable = False
        if request.user:
            user = request.user
            editable = (user.account == tweet.author)
            if page.creator.id is user.account.id:
                editable = True

        comments.append(tweet.get_tweet_front(editable, True))
    if request.user:
        can_write = request.user.account in page.get_all_admins()
    data = {'comments': comments, 'comments_json': json.dumps(comments), 'title': page.title,
            'can_write': can_write, 'description': page.description, 'page_id': page.page_id}
    return render(request, './twitting/commentsPage.html', data)


@login_required
def my_page(request):
    page = Page.objects.get(page_id=request.user.username)
    return get_page(request, page)


def get_tweet_page(request, tweet_id):
    q = Tweet.objects.filter(id=tweet_id)
    if not q.exist():
        return HttpResponse(status=404)
    tweet = Tweet.objects.get(id=tweet_id)
    editable = False
    if request.user:
        if request.user.account == tweet.author:
            editable = True
    comments = [tweet.get_tweet_front(editable, True)]
    data = {'comments': comments, 'comments_json': json.dumps(comments),
            'title': 'replies of ' + tweet.author.name + 'posts',
            'can_write': False}  # todo: check this shit!!!!
    return render(request, './twitting/commentsPage.html', data)
