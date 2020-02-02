import copy
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from paging.models import Page
from twitting.models import Tweet


@login_required
def page(request, page_id):
    personal_page = Page.objects.filter(Q(creator=request.user.account) & Q(personal_page=True)).first()
    tweets = Tweet.objects.filter(page=personal_page, parent_tweet=None)
    author = {
        'name': request.user.username,
        'avatar': 'https://avatars2.githubusercontent.com/u/45905632?s=460&v=4',
    }
    comments = []
    for tweet in tweets:
        comments.append({
            'bookmark_state': False,
            'like_pack': {
                'like_numbers': 10
            },
            'editable': True,
            'author': author,
            'content': tweet.document,
            'time': tweet.date_published.isoformat(),
            'replys': [],
            'id': 'tweet' + str(tweet.id)
        })
    data = {'comments': comments, 'comments_json': json.dumps(comments), 'tittle': request.user.username + ' page',
            'can_write': True}
    return render(request, './twitting/commentsPage.html', data)
